import logging
from typing import List,Optional
from fastapi import APIRouter, Form, Request, status, FastAPI, BackgroundTasks, Header, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from psycopg.rows import dict_row
from fastapi.responses import JSONResponse
from api.notification_services.notifications import put_email, send_email
from api.notification_services.model import  EmailNotificationModel
from datetime import datetime
from core import config
from utils.common import post_blob_client
from utils.utils import audit_trail
from utils.common import get_data_from_blob, post_blob_client, get_auth0_token, get_user_by_email, create_user, \
generate_password_change_ticket, fetch_user_id_by_email, generate_email_html
from core.config import WEB_APP_URL



# from utils.common import account_email_verification
import json
from uuid import UUID

from api.account.model import Account_Types, Accounts, \
    MasterAccountCategories, MasterClaims, MasterClaimsMicroservice, MasterClaimsusingid, MasterMicroServices, \
        MasterPolicies, MasterPoliciesRequest, PostRoles, Put_Account_overview, RoleWisePoliciesAndPermissions, Roles, UserAccounts,Policy,Post_Account_Types,Post_Account_confriguations, \
        AccountTypesByCategory, PartnerAccounts,CustomerAccounts, ServiceProviderAccounts, SupportAccounts, UpdateCustomerAccounts, UpdatePartnerAccounts, UpdateServiceProviderAccounts, UpdateSupportAccounts,UserRequestModel

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()

# @router.get('/account_types', status_code=status.HTTP_200_OK,
#              name="Get all accounts types", response_model=List[Account_Types])
# async def get_all_accounts_types(request: Request):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM accounts.account_types"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/account_types', status_code=status.HTTP_200_OK,
            name="Get account types by app_short_code", response_model=List[Account_Types])
async def get_account_types_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT ats.id, ats.app_short_code, ats.display_name, ats.short_code, 
                       mac.display_name AS account_category_display_name, 
                       ats.account_subcategory, ats.account_classification, 
                       ats.self_registration_allowed, acs.display_name AS parent_account_display_name
                FROM accounts.account_types ats
				LEFT JOIN accounts.account_types acs 
                ON ats.parent_account_type_id = acs.id
                JOIN accounts.master_account_categories mac 
                ON ats.account_category_id = mac.id 
                WHERE ats.app_short_code = %s
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

# @router.get('/accounts', status_code=status.HTTP_200_OK,
#              name="Get all accounts", response_model=List[Accounts])
# async def get_all_accounts(request: Request):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM accounts.accounts"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/accounts', status_code=status.HTTP_200_OK,
            name="Get accounts by app_short_code", response_model=List[Accounts])
async def get_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT acs.id, acs.app_short_code, acs.display_name, 
                              mac.display_name AS account_category_display_name, 
                              ats.display_name AS account_type_display_name, 
                              ats.account_subcategory, 
                              acs.address, acs.contactdetails, 
                              acs.logo_uri, acs.status, 
                              acs.parent_id, acs.grandparent_id 
                FROM accounts.accounts acs 
                JOIN accounts.master_account_categories mac 
                ON acs.account_category_id = mac.id 
                JOIN accounts.account_types ats 
                ON acs.account_type_id = ats.id 
                WHERE acs.app_short_code = %s""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/service_provider_accounts', status_code=status.HTTP_200_OK,
            name="Get Service Provider Accounts by app_short_code", response_model=List[Accounts])
async def get_service_provider_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT acs.id, acs.app_short_code, acs.display_name, acs.account_type_id,
                              mac.display_name AS account_category_display_name, 
                              ats.display_name AS account_type_display_name, 
                              ats.account_subcategory, 
                              acs.address, acs.contactdetails, 
                              acs.logo_uri, acs.status, 
                              acs.parent_id, acs.grandparent_id 
                FROM accounts.accounts acs 
                JOIN accounts.master_account_categories mac 
                ON acs.account_category_id = mac.id 
                JOIN accounts.account_types ats 
                ON acs.account_type_id = ats.id 
                WHERE acs.app_short_code = %s AND acs.account_category_id = 1""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/support_accounts', status_code=status.HTTP_200_OK,
            name="Get Support Accounts by app_short_code", response_model=List[Accounts])
async def get_support_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT acs.id, acs.app_short_code, acs.display_name, acs.account_type_id, 
                              mac.display_name AS account_category_display_name, 
                              ats.display_name AS account_type_display_name, 
                              ats.account_subcategory, 
                              acs.address, acs.contactdetails, 
                              acs.logo_uri, acs.status, 
                              acs.parent_id, acs.grandparent_id 
                FROM accounts.accounts acs 
                JOIN accounts.master_account_categories mac 
                ON acs.account_category_id = mac.id 
                JOIN accounts.account_types ats 
                ON acs.account_type_id = ats.id 
                WHERE acs.app_short_code = %s AND acs.account_category_id = 2""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/partner_accounts', status_code=status.HTTP_200_OK,
            name="Get Partner Accounts by app_short_code", response_model=List[Accounts])
async def get_partner_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT acs.id, acs.app_short_code, acs.display_name, acs.account_type_id,
                              mac.display_name AS account_category_display_name, 
                              ats.display_name AS account_type_display_name, 
                              ats.account_subcategory, 
                              acs.address, acs.contactdetails, 
                              acs.logo_uri, acs.status, 
                              acs.parent_id, acs.grandparent_id 
                FROM accounts.accounts acs 
                JOIN accounts.master_account_categories mac 
                ON acs.account_category_id = mac.id 
                JOIN accounts.account_types ats 
                ON acs.account_type_id = ats.id 
                WHERE acs.app_short_code = %s AND acs.account_category_id = 3""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/customer_accounts', status_code=status.HTTP_200_OK,
            name="Get Customer Accounts by app_short_code", response_model=List[Accounts])
async def get_customer_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT acs.id, acs.app_short_code, acs.display_name, acs.account_type_id,
                              mac.display_name AS account_category_display_name, 
                              ats.display_name AS account_type_display_name, 
                              ats.account_subcategory, 
                              acs.address, acs.contactdetails, 
                              acs.logo_uri, acs.status, 
                              acs.parent_id, acs.grandparent_id 
                FROM accounts.accounts acs 
                JOIN accounts.master_account_categories mac 
                ON acs.account_category_id = mac.id 
                JOIN accounts.account_types ats 
                ON acs.account_type_id = ats.id 
                WHERE acs.app_short_code = %s AND acs.account_category_id = 4""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.post("/accounts/customer_accounts", status_code=status.HTTP_200_OK, name="Create a Customer Account")
async def create_customer_account(request:Request, background_tasks: BackgroundTasks,
                                 customer_account: CustomerAccounts, app_short_code:str=Header(...,alias="app_short_code"),
                                 Origin: str = Header(None, alias="origin")):
    try:
        api_name = request.url.path
        api_operation = request.method
 
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(
            audit_trail, audit_trail_entry, request
        )
    except Exception as e:
        logger.error(f"Error in Audit Trail: {e}")
    try:
        address=json.dumps(customer_account.address.dict()) if customer_account.address else None
        contactdetails=json.dumps(customer_account.contactdetails.dict())
        logger.info(type(address))
        logger.info(type(contactdetails))
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    INSERT INTO accounts.accounts
                    (app_short_code, display_name, account_category_id, account_type_id,
                                               address, contactdetails, logo_uri, parent_id, grandparent_id)
                    VALUES (%s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s::uuid, %s::uuid) RETURNING *""",
                    (app_short_code, 
                     customer_account.display_name, 
                     customer_account.account_category_id,
                     customer_account.account_type_id,
                     address,
                     contactdetails,
                     customer_account.logo_uri,
                     customer_account.parent_id,
                     customer_account.grandparent_id,
                    ))
                result = await cur.fetchone()
                # email_send=await account_email_verification(result,request, Origin)
                logger.info("inserted in accounts table")
            if result is None:
                        return {
                                "status": False,
                                "detail": "Unable to add customer account entry."
                            }
            account = result
            logger.info(result)
            account_id=account["id"]
            contacts=account["contactdetails"]
            user_email=contacts["contactemail"]
            first_name=contacts["contactname"].split(" ")[0]
            last_name=contacts["contactname"].split(" ")[1] 
            account_types_id=account["account_type_id"]
            token = get_auth0_token()
            if token:
                    user_info = get_user_by_email(user_email, token)
                    if not user_info:
                        create_user(token, user_email, 'temp@123', first_name, last_name)
                        user_id = fetch_user_id_by_email(user_email, token)
                        ticket_url = generate_password_change_ticket(token, user_id, WEB_APP_URL)
                        change_password_email_data = EmailNotificationModel(
                        to=user_email,
                        subject="Password Reset Request for Your Account",
                        body=generate_email_html('reset', first_name, ticket_url))
                        send_email(change_password_email_data, request)
                        current_time = int(datetime.utcnow().timestamp())

                        logger.info(f"headers origin{Origin}")
            if not Origin:
                Origin = 'https://genaiot-dev.moschip-digitalsky.com'
            temp_url=Origin
            logger.info(f"{Origin},{temp_url}")

            verify_link = f"{temp_url}/verifyUser/{account_id}/accounts"
            logger.info(f"verify_link {verify_link}")

            email_data = EmailNotificationModel(
            to=user_email,
            subject="Customer Account Registered Successfully",
            body=generate_email_html('verify', first_name, verify_link))
            send_email(email_data, request)
            logger.info(f"Email notification sent to {email_data} user_account_id{account_id},account_types_id{account_types_id}")

            
            logger.info({"status": "success", "message": "Customer Account created successfully"})
            return {
                    "status": True,
                    "detail": "Customer Account created successfully.",
                    "customer_accounts": result
                }
    except Exception as e:
        logger.error(f"Account Insertion Error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
@router.get('/master_account_categories', status_code=status.HTTP_200_OK,
             name="Get all master account categories", response_model=List[MasterAccountCategories])
async def get_master_account_categories(request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT *
                FROM accounts.master_account_categories"""
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/master_claims', status_code=status.HTTP_200_OK,
             name="Get all master claims", response_model=List[MasterClaims])
async def get_master_claims(request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # await cur.execute("""
            #     SELECT *ut
            #     FROM accounts.master_claims"""
            # )
            await cur.execute("""
                SELECT mcs.id, mcs.feature_name, mcs.display_name, mcs.name, 
                       mcs.type, mcs.is_default_claim,
                       mms.display_name AS microservice_display_name
                FROM accounts.master_claims mcs 
                JOIN accounts.master_microservices mms 
                ON mcs.microservice_id = mms.id 
            """
            )
            results = await cur.fetchall()
            logger.info(results)
            return results
    
@router.post('/master_claims', name="insert a single entry in master claims",status_code=status.HTTP_200_OK)
async def create_master_claims(request: Request, background_tasks: BackgroundTasks,masterclaimsservice:MasterClaimsMicroservice):
    try:
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,   
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(
            audit_trail, audit_trail_entry, request
        )
    except Exception as e:
        logger.error("audit trail error")
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    INSERT INTO accounts.master_claims(
                        feature_name,
                        display_name ,
                        name ,
                        type ,
                        is_default_claim ,
                        microservice_id
                        )
                VALUES(%s,%s,%s,%s,%s,%s);
                        """, (
                            masterclaimsservice.feature_name,
                            masterclaimsservice.display_name,
                            masterclaimsservice.name,
                            masterclaimsservice.type,
                            masterclaimsservice.is_default_claim,
                            masterclaimsservice.microservice_id,
                        ) )
        #logger.info({"status": "success", "message": "Master Claims are created successfully"})
        return {"status": "success", "message": "Master Claims created successfully"}
    except Exception as e:
        logger.error(f"Master Claims Insertion Error {str(e)}")
        #logger.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put('/account/master_claims/{claims_id}', name="Update a single master claim", status_code=status.HTTP_200_OK)
async def update_master_claim_detail(claims_id: int, request: Request, background_tasks: BackgroundTasks, item: MasterClaimsMicroservice):
    try:
        # Set up the audit trail entry
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(audit_trail, audit_trail_entry, request)
    except Exception as e:
        logger.error("Audit trail error: %s", str(e))
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                # Validate if the claims_id exists
                await cur.execute("SELECT id FROM accounts.master_claims WHERE id = %s;", (claims_id,))
                claims_record = await cur.fetchone()
 
                if not claims_record:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Claims ID {claims_id} does not exist."
                    )
                # Perform the update if the ID exists
                await cur.execute(
                    """
                    UPDATE accounts.master_claims
                    SET
                        feature_name = COALESCE(%s, feature_name),
                        display_name = COALESCE(%s, display_name),
                        name = COALESCE(%s, name),
                        is_default_claim = COALESCE(%s, is_default_claim),
                        microservice_id = COALESCE(%s, microservice_id)
                    WHERE id = %s;
                    """,
                    (
                        item.feature_name,
                        item.display_name,
                        item.name,
                        item.is_default_claim,
                        item.microservice_id,
                        claims_id
                    )
                )
        return {"status": "success", "message": "Master Claims updated successfully"}
    except HTTPException as e:
        # Rethrow HTTPException to handle specific error messages
        raise e
    except Exception as e:
        logger.error("Master Claims update error: %s", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while updating master claims")
 

@router.get('/master_microservices', status_code=status.HTTP_200_OK,
             name="Get all master microservices", response_model=List[MasterMicroServices])
async def get_master_microservices(request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT *
                FROM accounts.master_microservices"""
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/master_policies', status_code=status.HTTP_200_OK,
             name="Get all master policies", response_model=List[MasterPolicies])
async def get_master_policies(request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # await cur.execute("""
            #     SELECT *
            #     FROM accounts.master_policies"""
            # )
            await cur.execute("""
                SELECT mps.id, mms.id AS microservice_id, mms.display_name AS microservice_display_name, 
                       mps.display_name, mps.claims, mps.menu, 
                       mps.permissions_required
                FROM accounts.master_policies mps 
                JOIN accounts.master_microservices mms 
                ON mps.microservice_id = mms.id 
            """
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.post('/account/master_policies', name="Insert a single policy", status_code=status.HTTP_200_OK)
async def insert_policy_detail(request: Request, background_tasks: BackgroundTasks, policy: MasterPoliciesRequest):
    try:
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(
            audit_trail, audit_trail_entry, request
        )
    except Exception as e:
        logger.error("Audit trail error: %s", str(e))
    try:
        print(policy.claims.dict(),policy.menu,"policypolicypolicy")
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    INSERT INTO accounts.master_policies(
                        microservice_id,
                        display_name,
                        claims,
                        menu,
                        permissions_required
                    )
                    VALUES (%s, %s, %s, %s, %s);
                """, (

                    policy.microservice_id,
                    policy.display_name,
                    policy.claims.json(),
                    policy.menu.json(),
                    policy.permissions_required
                ))
        #logger.info({"status": "success", "message": "Policy created successfully"})
        return {"status": "success", "message": "Policy created successfully"}
    except Exception as e:
        logger.error("Policy Insertion Error: %s", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put('/accounts/master_policies/{policy_id}', name="Update a single policy", status_code=status.HTTP_200_OK)
async def update_policy_detail(policy_id: str, request: Request, background_tasks: BackgroundTasks, policy: MasterPoliciesRequest):
    try:
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(
            audit_trail, audit_trail_entry, request
        )
    except Exception as e:
        logger.error("Audit trail error: %s", str(e))
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                # Validate if the policy_id exists
                await cur.execute("""
                    SELECT id FROM accounts.master_policies WHERE id = %s;
                """, (policy_id,))
                policy_record = await cur.fetchone()
                if not policy_record:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Policy ID {policy_id} does not exist."
                    )
                # Update the policy if it exists
                await cur.execute("""
                    UPDATE accounts.master_policies
                    SET
                        microservice_id = %s,
                        display_name = %s,
                        claims = %s,
                        menu = %s,
                        permissions_required = %s
                    WHERE id = %s;
                """, (
                    policy.microservice_id,
                    policy.display_name,
                    policy.claims.json(),
                    policy.menu.json(),
                    policy.permissions_required,
                    policy_id
                ))
        return {"status": "success", "message": "Policy updated successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Policy Update Error: %s", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
# @router.get('/role_wise_policies_and_permissions', status_code=status.HTTP_200_OK,
#              name="Get all role wise policies and permissions",
#              response_model=List[RoleWisePoliciesAndPermissions])
# async def get_all_role_wise_policies_and_permissions(request: Request):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM accounts.role_wise_policies_and_permissions"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/role_wise_policies_and_permissions',
            status_code=status.HTTP_200_OK,
            name="Get role wise policies and permissions by app_short_code",
            response_model=List[RoleWisePoliciesAndPermissions])
async def get_role_wise_policies_and_permissions_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM accounts.role_wise_policies_and_permissions WHERE app_short_code = %s""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

# @router.get('/roles', status_code=status.HTTP_200_OK, name="Get all roles",
#              response_model=List[Roles])
# async def get_all_roles(request: Request):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM accounts.roles"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/roles', status_code=status.HTTP_200_OK,
            name="Get roles by app_short_code", response_model=List[Roles])
async def get_roles_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT rs.id, rs.app_short_code, ats.display_name AS account_type_name, 
                              rs.display_name, rs.is_it_admin_role
                FROM accounts.roles rs 
                JOIN accounts.account_types ats 
                ON rs.account_type_id::INTEGER = ats.id 
                WHERE rs.app_short_code = %s
                AND rs.display_name != 'Super Admin'
            """, (app_short_code,))
            
            results = await cur.fetchall()
            logger.info(results)
            return results

# @router.get('/user_accounts', status_code=status.HTTP_200_OK,
#              name="Get all user accounts", response_model=List[UserAccounts])
# async def get_all_user_accounts(request: Request):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM accounts.user_accounts"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/user_accounts', status_code=status.HTTP_200_OK,
            name="Get user accounts by app_short_code", response_model=List[UserAccounts])
async def get_user_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM accounts.user_accounts WHERE app_short_code = %s""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results


@router.get('/roles/{roleid}/permissions', status_code=status.HTTP_200_OK,
            name="Get role-based permissions", response_model=List[Policy])
async def get_role_permissions(roleid: int, request: Request):
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                
                query="""                    
                SELECT json_agg(
                        json_build_object(
                            'msid', ms.id,
                            'name', ms.display_name,
                            'policies', (
                                SELECT json_agg(
                                    json_build_object(
                                        'mpid', mp.id,
                                        'name', mp.display_name,
                                        'policyId', mp.microservice_id,
                                        'rwppid', rwpp.id,
                                        'role_id', rwpp.role_id,
                                        'permission', rwpp.policy_permissions->'Scope'->0
                                    )
                                )
                                FROM accounts.master_policies mp
                                JOIN accounts.role_wise_policies_and_permissions rwpp 
                                    ON mp.microservice_id = rwpp.policy_id
                                WHERE rwpp.role_id = %s AND mp.microservice_id = ms.id
                            )
                        )
                    ) as result
                    FROM accounts.master_microservices ms;"""
                await cur.execute(query, (roleid,))
                result = await cur.fetchall()
                logger.info(f"result after fetching: {result}")

                # print((result),type(result[0]['result']) )
                if result and result[0]['result']:
                    return JSONResponse(content={"msg": 'Policies & Scope found',"status":True, "Data": result[0]['result']}, status_code=status.HTTP_200_OK)
                    # return result[0]['result']

                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No policies found for the given role ID. {result}")                    
    except Exception as e:
        logger.error(f"Error occurred in except: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while processing the request: {e}")


@router.post('/account_types', name="insert a single entry in account types", status_code=status.HTTP_200_OK, )
async def create_account_type(request: Request, policy:Post_Account_Types,app_short_code: str = Header(..., alias="app_short_code")):
    try:
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        BackgroundTasks.add_task(audit_trail, audit_trail_entry, request)
    except Exception as e:
        logger.error("audit trail error")
 
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    INSERT INTO accounts.account_types(
                            app_short_code,
                            display_name,
                            short_code,
                            account_category_id,
                            account_subcategory,
                            account_classification,
                            self_registration_allowed,
                            parent_account_type_id)
                VALUES(%s,%s, %s, %s, %s, %s, %s, %s) RETURNING *"""
                            , (
                            app_short_code,
                            policy.display_name,
                            policy.short_code,
                            policy.account_category_id,
                            policy.account_subcategory,
                            policy.account_classification,
                            policy.self_registration_allowed,
                            policy.parent_account_type_id
                        ) )
        #logger.info({"status": "success", "message": "Account Type created successfully"})
                result = await cur.fetchone()
                if result is None:
                            return {
                                "status": False,
                                "detail": "Unable to add account type entry."
                            }
                logger.info({"status": "success", "message": "Account Type created successfully"})
                return {
                    "status": True,
                    "detail": "Account Type created successfully.",
                    "account_type": result
                }
    except Exception as e:
        logger.error(f"Account Type Insertion Error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 
@router.put('/account_types/{id}', name="update existing account type", status_code=status.HTTP_200_OK)
async def update_account_type_detail(request: Request, background_tasks: BackgroundTasks, id: int, policy: Post_Account_Types, app_short_code: str = Header(..., alias="app_short_code")):
    try:
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(audit_trail, audit_trail_entry, request)
    except Exception as e:
        logger.error("audit trail error")
 
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    UPDATE accounts.account_types SET
                            app_short_code=%s,
                            display_name=%s,
                            short_code=%s,
                            account_category_id=%s,
                            account_subcategory=%s,
                            account_classification=%s,
                            self_registration_allowed=%s,
                            parent_account_type_id=%s
                    WHERE id = %s RETURNING *
                """, (
                            app_short_code,
                            policy.display_name,
                            policy.short_code,
                            policy.account_category_id,
                            policy.account_subcategory,
                            policy.account_classification,
                            policy.self_registration_allowed,
                            policy.parent_account_type_id,
                            id
                ))
                result = await cur.fetchone()
                if result is None:
                            return {
                                "status": False,
                                "detail": "Unable to update account type entry."
                            }

                logger.info({"status": "success", "message": "Account Type updated successfully"})
                return {
                    "status": True,
                    "detail": "Account Type updated successfully.",
                    "account_type": result
                }
    except Exception as e:
        logger.error(f"Account Type Update Error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.put('/accounts/app_confriguations', name="update existing account confriguations", status_code=status.HTTP_200_OK)
async def update_account_confriguations(request: Request, background_tasks: BackgroundTasks,confriguations: Post_Account_confriguations, app_short_code: str = Header(..., alias="app_short_code")):
    try:
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(audit_trail, audit_trail_entry, request)
    except Exception as e:
        logger.error("audit trail error")
 
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(""" UPDATE applications.applications SET
                    is_site = COALESCE(%s, is_site),
                    is_fleet = COALESCE(%s, is_fleet),
                    is_super_asset = COALESCE(%s, is_super_asset)
                WHERE short_code = %s returning is_site,is_fleet,is_super_asset;""",      
                (
                            confriguations.is_site,
                            confriguations.is_fleet,
                            confriguations.is_super_asset,
                            app_short_code
                ))
                result = await cur.fetchone()
                # logger.info(f"result{result}")
                if result is None:
                            return {
                                "status": False,
                                "detail": "Unable to update applications entry.", "data": result
                            }

                return {
                    "status": True,
                    "detail": "Applications Confriguation updated successfully.",
                    "data": result
                }
    except Exception as e:
        logger.error(f"Applications Update Error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Applications Update Error{e}")
    
@router.post('/roles', name="Create a Roles", status_code=status.HTTP_200_OK)
async def create_roles(request: Request, roles:PostRoles, background_tasks: BackgroundTasks):
    try:
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(audit_trail, audit_trail_entry, request)
    except Exception as e:
        logger.error("Audit trail error")
 
    try:
       async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO accounts.roles (
                            app_short_code,
                            account_type_id,
                            display_name,
                            is_it_admin_role
                        ) VALUES (%s, %s, %s, %s) RETURNING *
                """, (
                    roles.app_short_code,
                    roles.account_type_id,
                    roles.display_name,
                    roles.is_it_admin_role
                ))
                result = await cur.fetchone()
                if result is None:
                    return {"status": False, "detail": "Unable to create roles entry."}
 
                logger.info({"status": "success", "message": "Roles created successfully"})
                return {"status": True, "detail": "Roles created successfully", "roles": result}
    except Exception as e:
        logger.error(f"Roles Insertion Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
# Update API
@router.put('/roles/{role_id}', name="Update Roles Settings", status_code=status.HTTP_200_OK)
async def update_roles(request: Request, role_id:int, roles:PostRoles, background_tasks: BackgroundTasks):
    try:
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(audit_trail, audit_trail_entry, request)
    except Exception as e:
        logger.error("Audit trail error")
 
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    UPDATE accounts.roles SET
                            app_short_code=%s,
                            account_type_id=%s,
                            display_name=%s,
                            is_it_admin_role=%s
                    WHERE id = %s RETURNING *
                """, (
                    roles.app_short_code,
                    roles.account_type_id,
                    roles.display_name,
                    roles.is_it_admin_role,
                    role_id
 
                ))
                result = await cur.fetchone()
                if result is None:
                    return {"status": False, "detail": "Unable to update Roles entry."}
 
                logger.info({"status": "success", "message": "Roles updated successfully"})
                return {"status": True, "detail": "Roles updated successfully", "roles": result}
    except Exception as e:
        logger.error(f"Roles Update Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    

@router.put('/accounts/app_overview', name="update existing account overview", status_code=status.HTTP_200_OK)
async def update_app_overview(request: Request, background_tasks: BackgroundTasks,overview: Put_Account_overview = Form(media_type="multipart/form-data"), app_short_code: str = Header(..., alias="app_short_code")):
    try:
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(audit_trail, audit_trail_entry, request)
    except Exception as e:
        logger.error("audit trail error")
    if overview.icon_uri:
            try:
                icon_url_content = await overview.icon_uri.read()
                icon_url_name = f"{config.ICON_CONTAINER_NAME}/{app_short_code}.{overview.icon_uri.filename.split('.')[-1]}"
                icon_name = f"{app_short_code}.{overview.icon_uri.filename.split('.')[-1]}"
                await post_blob_client(config.ICON_CONTAINER_NAME,
                                        icon_name,
                                        icon_url_content,
                                        request)
            except Exception as e:
                logger.error(f"Failed to upload ICON image: {str(e)}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to upload IoT architecture image.{str(e)}")

            logger.info(f"ICON uploaded to Azure Blob Storage:\n1.{icon_url_name}")

    else: 
        icon_url_name=None

    if overview.logo_uri:
        try:
            logo_url_content = await overview.logo_uri.read()
            logo_url_name =f"{config.LOGO_CONTAINER_NAME}/{app_short_code}.{overview.logo_uri.filename.split('.')[-1]}"
            logo_name =f"{app_short_code}.{overview.logo_uri.filename.split('.')[-1]}"

            await post_blob_client(config.LOGO_CONTAINER_NAME,
                                    logo_name,
                                    logo_url_content,
                                    request)
        except Exception as e:
            logger.error(f"Failed to upload LOGO image: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to upload LOGO image.{str(e)}")

        logger.info(f"LOGO uploaded to Azure Blob Storage:\n1.{logo_url_name}")

    else: 
        logo_url_name=None


 
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                WITH app_update AS (
                    UPDATE applications.applications
                    SET
                        icon_uri = COALESCE(%s, icon_uri),
                        description = COALESCE(%s, description)
                    WHERE short_code = %s
                    RETURNING short_code
                )
                UPDATE accounts.accounts
                SET
                    logo_uri = COALESCE(%s, logo_uri)
                WHERE app_short_code = (SELECT short_code FROM app_update);
                """, (icon_url_name, overview.description, app_short_code, logo_url_name))
                return {
                    "status": True,
                    "detail": "Applications overview updated successfully."
                }
    except Exception as e:
        logger.error(f"Applications Update Error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Applications Update Error{e}")



@router.get('/verifyUserprev/{user_id}', status_code=status.HTTP_200_OK, name="Verify user from email link")
async def verify_user(user_id: str, request: Request):
    try:
        # Query the database to get the user details by user_id
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""SELECT * FROM accounts.user_accounts WHERE id = %s""", (user_id,))
                results = await cur.fetchone()
                logger.info(f"user found {results['verify_url_time']}{results}")
                # return
                if  results is None:
                    return JSONResponse(content={"message": "User not found","data":results}, status_code=status.HTTP_404_NOT_FOUND)                                
                if  results['user_status'] :
                    return JSONResponse(content={"message": "Already Verified","user_status":results['user_status']}, status_code=status.HTTP_200_OK)                                
                
                current_time = int(datetime.utcnow().timestamp())
                time_difference = current_time - results['verify_url_time']

                if time_difference > 86400:
                    logger.info(f"link expired {time_difference}")
                    return JSONResponse(content={"message": "Verification link expired","time_difference":time_difference,"user_status":False}, status_code=status.HTTP_200_OK)
                    # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Verification link expired {time_difference}")

                # If not verified, update the user_status to True
                await cur.execute("""UPDATE accounts.user_accounts SET user_status = TRUE WHERE id = %s returning user_status""", (user_id,))
                result = await cur.fetchone()
                if result is None:
                    return JSONResponse(content={"message": "User not verified successfully","user_status":False}, status_code=status.HTTP_200_OK)
                else:
                    return JSONResponse(content={"message": "User verified successfully","user_status":result['user_status']}, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error occurred during verification: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while processing the verification request: {e}")

@router.get(
    '/account_types/{account_category_id}',
    status_code=status.HTTP_200_OK,
    name="Get account types by app_short_code and account_category_id",
    response_model=List[AccountTypesByCategory]
)
async def get_account_types_by_app_short_code_and_category(
    request: Request,
    app_short_code: str = Header(..., alias="app_short_code"),
    account_category_id: int = Path(..., title="Account Category ID")
):
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(
                    """
                    SELECT display_name AS name, id AS value 
                    FROM accounts.account_types
                    WHERE account_category_id = %s AND app_short_code = %s
                    """,
                    (account_category_id, app_short_code)
                )
                results = await cur.fetchall()
                
                if not results:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No account types found for the specified app_short_code and account_category_id."
                    )
                
                return results
                
    except Exception as e:
        logger.error(f"Error fetching account types: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while fetching account types."
        )
@router.post("/accounts/partner_accounts", status_code=status.HTTP_200_OK, name="Create a Partner Account")
async def create_partner_account(request:Request, background_tasks: BackgroundTasks,
                                 partner_account: PartnerAccounts, app_short_code:str=Header(...,alias="app_short_code"),
                                 Origin: str = Header(None, alias="origin")):
    try:
        api_name = request.url.path
        api_operation = request.method
 
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(
            audit_trail, audit_trail_entry, request
        )
    except Exception as e:
        logger.error(f"Error in Audit Trail: {e}")
    try:
        address=json.dumps(partner_account.address.dict()) if partner_account.address else None
        contactdetails=json.dumps(partner_account.contactdetails.dict())
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    INSERT INTO accounts.accounts
                    (app_short_code, display_name, account_category_id, account_type_id,
                                               address, contactdetails, logo_uri, parent_id, grandparent_id)
                    VALUES (%s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s::uuid, %s::uuid) RETURNING *""",
                    (app_short_code, partner_account.display_name, partner_account.account_category_id,
                     partner_account.account_type_id,address,contactdetails,
                     partner_account.logo_uri,partner_account.parent_id, partner_account.grandparent_id))
                result = await cur.fetchone()
                # email_send=await account_email_verification(result,request, Origin)
            if result is None:
                        return {
                                "status": False,
                                "detail": "Unable to add partner account entry."
                            }
            account = result
            account_id=account["id"]
            contacts=account["contactdetails"]
            user_email=contacts["contactemail"]
            first_name=contacts["contactname"].split(" ")[0]
            last_name=contacts["contactname"].split(" ")[1]
            account_types_id=account["account_type_id"]
            token = get_auth0_token()
            if token:
                    user_info = get_user_by_email(user_email, token)
                    if not user_info:
                        create_user(token, user_email, 'temp@123', first_name, last_name)
                        user_id = fetch_user_id_by_email(user_email, token)
                        ticket_url = generate_password_change_ticket(token, user_id, WEB_APP_URL)
                        change_password_email_data = EmailNotificationModel(
                        to=user_email,
                        subject="Password Reset Request for Your Account",
                        body=generate_email_html('reset', first_name, ticket_url))
                        send_email(change_password_email_data, request)
                        current_time = int(datetime.utcnow().timestamp())

                        logger.info(f"headers origin{Origin}")
            if not Origin:
                Origin = 'https://genaiot-dev.moschip-digitalsky.com'
            temp_url=Origin
            logger.info(f"{Origin},{temp_url}")

            verify_link = f"{temp_url}/verifyUser/{account_id}/accounts"
            logger.info(f"verify_link {verify_link}")

            email_data = EmailNotificationModel(
            to=user_email,
            subject="Partner Account Registered Successfully",
            body=generate_email_html('verify', first_name, verify_link))
            send_email(email_data, request)
            logger.info(f"Email notification sent to {email_data} user_account_id{account_id},account_types_id{account_types_id}")

            logger.info({"status": "success", "message": "Partner Account created successfully"})
            return {
                    "status": True,
                    "detail": "Partner Account created successfully.",
                    "partner_accounts": result
                }
    except Exception as e:
        logger.error(f"Partner Account Insertion Error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@router.post("/accounts/service_provider_accounts", status_code=status.HTTP_200_OK, name="Create a Service Provider Account")
async def create_service_provider_account(request:Request, background_tasks: BackgroundTasks,
                                 service_provider_account: ServiceProviderAccounts, app_short_code:str=Header(...,alias="app_short_code"),
                                Origin: str = Header(None, alias="origin")):
    try:
        api_name = request.url.path
        api_operation = request.method
 
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(
            audit_trail, audit_trail_entry, request
        )
    except Exception as e:
        logger.error(f"Error in Audit Trail: {e}")
    try:
        address=json.dumps(service_provider_account.address.dict()) if service_provider_account.address else None
        contactdetails=json.dumps(service_provider_account.contactdetails.dict())
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    INSERT INTO accounts.accounts
                    (app_short_code, display_name, account_category_id, account_type_id,
                                               address, contactdetails, logo_uri, parent_id, grandparent_id)
                    VALUES (%s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s::uuid, %s::uuid) RETURNING *""",
                    (app_short_code, service_provider_account.display_name, service_provider_account.account_category_id,
                     service_provider_account.account_type_id,address,contactdetails,
                     service_provider_account.logo_uri, service_provider_account.parent_id, service_provider_account.grandparent_id))
                result = await cur.fetchone()
            if result is None:
                        return {
                                "status": False,
                                "detail": "Unable to add service provider account entry."
                            }
            account = result
            account_id=account["id"]
            contacts=account["contactdetails"]
            user_email=contacts["contactemail"]
            first_name=contacts["contactname"].split(" ")[0]
            last_name=contacts["contactname"].split(" ")[1]
            account_types_id=account["account_type_id"]
            token = get_auth0_token()
            if token:
                    user_info = get_user_by_email(user_email, token)
                    if not user_info:
                        create_user(token, user_email, 'temp@123', first_name, last_name)
                        user_id = fetch_user_id_by_email(user_email, token)
                        ticket_url = generate_password_change_ticket(token, user_id, WEB_APP_URL)
                        change_password_email_data = EmailNotificationModel(
                        to=user_email,
                        subject="Password Reset Request for Your Account",
                        body=generate_email_html('reset', first_name, ticket_url))
                        send_email(change_password_email_data, request)
                        current_time = int(datetime.utcnow().timestamp())

                        logger.info(f"headers origin{Origin}")
            if not Origin:
                Origin = 'https://genaiot-dev.moschip-digitalsky.com'
            temp_url=Origin
            logger.info(f"{Origin},{temp_url}")

            verify_link = f"{temp_url}/verifyUser/{account_id}/accounts"
            logger.info(f"verify_link {verify_link}")

            email_data = EmailNotificationModel(
            to=user_email,
            subject="Service Provider Account Registered Successfully",
            body=generate_email_html('verify', first_name, verify_link))
            send_email(email_data, request)
            logger.info(f"Email notification sent to {email_data} user_account_id{account_id},account_types_id{account_types_id}")

            logger.info({"status": "success", "message": "Service Provider Account created successfully"})
            return {
                    "status": True,
                    "detail": "Service Provider Account created successfully.",
                    "service_provider_accounts": result
                }
    except Exception as e:
        logger.error(f"Service Provider Account Insertion Error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.post("/accounts/support_accounts", status_code=status.HTTP_200_OK, name="Create a Support Account")
async def create_support_account(request:Request, background_tasks: BackgroundTasks,
                                 support_accounts: SupportAccounts, app_short_code:str=Header(...,alias="app_short_code"),
                                  Origin: str = Header(None, alias="origin")):
    try:
        api_name = request.url.path
        api_operation = request.method
 
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(
            audit_trail, audit_trail_entry, request
        )
    except Exception as e:
        logger.error(f"Error in Audit Trail: {e}")
    try:
        address=json.dumps(support_accounts.address.dict()) if support_accounts.address else None
        contactdetails=json.dumps(support_accounts.contactdetails.dict())
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    INSERT INTO accounts.accounts
                    (app_short_code, display_name, account_category_id, account_type_id,
                     address, contactdetails, logo_uri, parent_id, grandparent_id)
                    VALUES (%s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s::uuid, %s::uuid) RETURNING *""",
                    (app_short_code, support_accounts.display_name, support_accounts.account_category_id,
                     support_accounts.account_type_id,address,contactdetails,
                     support_accounts.logo_uri,  support_accounts.parent_id, support_accounts.grandparent_id))
                result = await cur.fetchone()
                # email_send=await account_email_verification(result,request, Origin)
            if result is None:
                        return {
                                "status": False,
                                "detail": "Unable to add Support account entry."
                            }
            account = result
            account_id=account["id"]
            contacts=account["contactdetails"]
            user_email=contacts["contactemail"]
            first_name=contacts["contactname"].split(" ")[0]
            last_name=contacts["contactname"].split(" ")[1]
            account_types_id=account["account_type_id"]
            token = get_auth0_token()
            if token:
                    user_info = get_user_by_email(user_email, token)
                    if not user_info:
                        create_user(token, user_email, 'temp@123', first_name, last_name)
                        user_id = fetch_user_id_by_email(user_email, token)
                        ticket_url = generate_password_change_ticket(token, user_id, WEB_APP_URL)
                        change_password_email_data = EmailNotificationModel(
                        to=user_email,
                        subject="Password Reset Request for Your Account",
                        body=generate_email_html('reset', first_name, ticket_url))
                        send_email(change_password_email_data, request)
                        current_time = int(datetime.utcnow().timestamp())

                        logger.info(f"headers origin{Origin}")
            if not Origin:
                Origin = 'https://genaiot-dev.moschip-digitalsky.com'
            temp_url=Origin
            logger.info(f"{Origin},{temp_url}")

            verify_link = f"{temp_url}/verifyUser/{account_id}/accounts"
            logger.info(f"verify_link {verify_link}")

            email_data = EmailNotificationModel(
            to=user_email,
            subject="Support Account Registered Successfully",
            body=generate_email_html('verify', first_name, verify_link))
            send_email(email_data, request)
            logger.info(f"Email notification sent to {email_data} user_account_id{account_id},account_types_id{account_types_id}")

            logger.info({"status": "success", "message": "Support Account created successfully"})
            return {
                    "status": True,
                    "detail": "Support Account created successfully.",
                    "support_accountss": result
                }
    except Exception as e:
        logger.error(f"Account Insertion Error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.put("/accounts/partner_accounts/{account_id}", status_code=status.HTTP_200_OK, name="Update a Partner Account")
async def update_partner_account(request:Request, background_tasks: BackgroundTasks,account_id: UUID,
                                 partner_account: UpdatePartnerAccounts, app_short_code:str=Header(...,alias="app_short_code"), ):
    try:
        api_name = request.url.path
        api_operation = request.method
 
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(
            audit_trail, audit_trail_entry, request
        )
    except Exception as e:
        logger.error(f"Error in Audit Trail: {e}")

    try:
        address=json.dumps(partner_account.address.dict()) if partner_account.address else None
        contactdetails=json.dumps(partner_account.contactdetails.dict())
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    UPDATE accounts.accounts
                    SET app_short_code=%s, display_name=%s, account_type_id=%s,
                                               address=%s::jsonb, contactdetails=%s::jsonb, logo_uri=%s, grandparent_id=%s::uuid
                    WHERE id=%s::uuid RETURNING *""",
                    (app_short_code, partner_account.display_name,
                     partner_account.account_type_id,address,contactdetails,
                     partner_account.logo_uri,partner_account.grandparent_id, account_id))
                result = await cur.fetchone()
            if result is None:
                        return {
                                "status": False,
                                "detail": "Unable to update partner account entry."
                            }
            logger.info({"status": "success", "message": "Partner Account updated successfully"})
            return {
                    "status": True,
                    "detail": "Partner Account updated successfully.",
                    "partner_accounts": result
                }
    except Exception as e:
        logger.error(f"Partner Account Updaytion Error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.put("/accounts/support_accounts/{account_id}", status_code=status.HTTP_200_OK, name="Update a Support Account")
async def update_support_account(account_id: UUID, request: Request, background_tasks: BackgroundTasks,
                                 support_accounts: UpdateSupportAccounts, app_short_code: str = Header(..., alias="app_short_code")):
    try:
        # Logging the audit trail
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(
            audit_trail, audit_trail_entry, request
        )
    except Exception as e:
        logger.error(f"Error in Audit Trail: {e}")
 
    try:
        # Connect to the database and update the support account
        address=json.dumps(support_accounts.address.dict()) if support_accounts.address else None
        contactdetails=json.dumps(support_accounts.contactdetails.dict())
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    UPDATE accounts.accounts
                    SET app_short_code = %s, display_name = %s,account_type_id = %s, address = %s::jsonb, contactdetails = %s::jsonb,
                        logo_uri = %s, grandparent_id = %s::uuid
                    WHERE id = %s RETURNING *
                """, (
                    app_short_code, support_accounts.display_name,support_accounts.account_type_id, address,
                    contactdetails, support_accounts.logo_uri, support_accounts.grandparent_id,
                    account_id
                ))
                result = await cur.fetchone()
           
            if result is None:
                return {
                    "status": False,
                    "detail": "Support account not found or no update made."
                }
 
            logger.info({"status": "success", "message": "Support Account updated successfully"})
            return {
                "status": True,
                "detail": "Support Account updated successfully.",
                "support_account": result
            }
    except Exception as e:
        logger.error(f"Account Update Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
    
@router.put("/accounts/customer_accounts/{account_id}", status_code=status.HTTP_200_OK, name="Update a Customer Account")
async def update_customer_account(account_id: UUID, request: Request, background_tasks: BackgroundTasks,
                                  customer_account: UpdateCustomerAccounts, app_short_code: str = Header(..., alias="app_short_code")):
    try:
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
 
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(
            audit_trail, audit_trail_entry, request
        )
    except Exception as e:
        logger.error(f"Error in Audit Trail: {e}")
 
    try:
        address=json.dumps(customer_account.address.dict()) if customer_account.address else None
        contactdetails=json.dumps((customer_account.contactdetails.dict()))
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    UPDATE accounts.accounts
                    SET app_short_code = %s,
                        display_name = %s,
                        account_type_id = %s,
                        address = %s::jsonb,
                        contactdetails = %s::jsonb,
                        logo_uri = %s,
                        grandparent_id = %s::uuid
                    WHERE  id = %s
                    RETURNING *""",
                    (
                        app_short_code,
                        customer_account.display_name,
                        customer_account.account_type_id,
                        address,
                        contactdetails,
                        customer_account.logo_uri,
                        customer_account.grandparent_id,
                        account_id
                    )
                )
                result = await cur.fetchone()
 
            if result is None:
                return {
                    "status": False,
                    "detail": "Unable to update customer account entry or account not found."
                }
 
            logger.info({"status": "success", "message": "Customer Account updated successfully"})
            return {
                "status": True,
                "detail": "Customer Account updated successfully.",
                "updated_account": result
            }
    except Exception as e:
        logger.error(f"Account Update Error {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.put("/accounts/service_provider_accounts/{account_id}", status_code=status.HTTP_200_OK, name="Update a Service Provider Account")
async def update_service_provider_account(account_id: UUID, request: Request, background_tasks: BackgroundTasks,
                                          service_provider_account: UpdateServiceProviderAccounts, app_short_code: str = Header(..., alias="app_short_code")):
    try:
        # Logging the audit trail
        api_name = request.url.path
        api_operation = request.method
        username = request.headers.get("CO-Email")
        audit_trail_entry = {
            "user": username,
            "api": api_name,
            "useractivity": f"{api_operation} {api_name}",
        }
        background_tasks.add_task(
            audit_trail, audit_trail_entry, request
        )
    except Exception as e:
        logger.error(f"Error in Audit Trail: {e}")
 
    try:
        # Connect to the database and update the service provider account
        address=json.dumps(service_provider_account.address.dict()) if service_provider_account.address else None
        contactdetails=json.dumps(service_provider_account.contactdetails.dict())
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    UPDATE accounts.accounts
                    SET app_short_code = %s, display_name = %s,account_type_id = %s, address = %s::jsonb, contactdetails = %s::jsonb,
                        logo_uri = %s, grandparent_id = %s::uuid
                    WHERE id = %s RETURNING *
                """, (
                    app_short_code, service_provider_account.display_name,service_provider_account.account_type_id,address,contactdetails, 
                    service_provider_account.logo_uri,service_provider_account.grandparent_id,
                    account_id
                ))
                result = await cur.fetchone()
           
            if result is None:
                return {
                    "status": False,
                    "detail": "Service Provider account not found or no update made."
                }
 
            logger.info({"status": "success", "message": "Service Provider Account updated successfully"})
            return {
                "status": True,
                "detail": "Service Provider Account updated successfully.",
                "service_provider_account": result
            }
    except Exception as e:
        logger.error(f"Account Update Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
    
@router.get('/accounts/get_role_display_name/{account_types_id}',status_code=status.HTTP_200_OK,name="Get the Role Display Name by using Account types id")
async def get_role_name_by_account_types_id(request:Request, account_types_id:int, app_short_code:str=Header(..., alias=("app_short_code"))):
    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                SELECT * FROM accounts.account_types WHERE app_short_code=%s AND id=%s
                    """,(app_short_code, account_types_id))
                result=await cur.fetchone()
                logger.info(result)
                if result is None:
                    return {"status":False, 
                            "message":"app short code or id is not found"}
                await cur.execute("""
                SELECT id, display_name FROM accounts.roles WHERE account_type_id=%s AND app_short_code=%s
                """, (str(account_types_id), app_short_code))
                data=await cur.fetchall()
                logger.info(data)
                if data is None:
                    return {
                        'status':False,
                        'message':'No data found'
                    }
                else:
                    return {'status':True, 
                            'data':data }

    except Exception as e:
        logger.error("Internal Server Error",{str(e)})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
    
@router.get('/master_claims/{microservice_id}', 
            status_code=status.HTTP_200_OK, 
            name="Get claims by microservice ID", 
            response_model=List[MasterClaimsusingid])
async def get_master_claims_by_microservice_id(request: Request, microservice_id: int):

    """
    API to fetch all claims from accounts.master_claims filtered by microservice_id.
    """
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
           await cur.execute("""
                SELECT mcs.id, mcs.feature_name, mcs.display_name, mcs.name, 
                       mcs.type, mcs.is_default_claim,
                       mms.display_name AS microservice_display_name,mcs.microservice_id
                FROM accounts.master_claims mcs 
                JOIN accounts.master_microservices mms 
                ON mcs.microservice_id = mms.id WHERE mcs.microservice_id=%s
            """,(microservice_id,))
           results = await cur.fetchall()
        logger.info(results[0])
        if not results:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No claims found for microservice_id {microservice_id}.")
        logger.info(f"Fetched {len(results)} claims for microservice_id {microservice_id}.")
        return results
    

    

@router.post(
    "/accounts/user_accounts",
    status_code=status.HTTP_200_OK,
    name="To insert into accounts.user_accounts data under the accounts like service, partner, support",
)
async def post_user_data(
    request: Request, background_tasks: BackgroundTasks, user_request_accounts: UserRequestModel,Origin: str = Header(None, alias="origin")
):
    api_name = request.url.path
    api_operation = request.method
    username = request.headers.get("CO-Email")

    audit_trail_entry = {
        "user": username,
        "api": api_name,
        "useractivity": f"{api_operation} {api_name}",
    }
    background_tasks.add_task(audit_trail, audit_trail_entry, request)

    try:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                try:
                    await cur.execute(
                        """
                    CALL accounts.manage_user_accounts_actions(
                        _action => %s,
                        _account_id => %s,
                        _app_short_code => %s,
                        _user_email => %s,
                        _user_login => %s,
                        _first_name => %s,
                        _user_mobile => %s,
                        _user_roleid => %s,
                        _verify_url_time => %s,
                        _middle_name => %s,
                        _last_name => %s,
                        _user_fullname => %s
                    )
                """,
                        (
                            "User_Accounts",
                            user_request_accounts.account_id,
                            user_request_accounts.app_short_code,
                            user_request_accounts.user_email,
                            user_request_accounts.user_email.split("@")[0],
                            user_request_accounts.first_name,
                            user_request_accounts.user_mobile,
                            user_request_accounts.user_roleid,
                            int(datetime.utcnow().timestamp()),
                            user_request_accounts.middle_name,
                            user_request_accounts.last_name,
                            user_request_accounts.user_fullname
                      )
                    )
                    result = await cur.fetchone()
                    # logger.info(f"Procedure result: {result['msg']}")
                    print(result)
                    user_account_id=result["msg"].split(":")[1]
                    token = get_auth0_token()
                    if token:
                        user_info = get_user_by_email(user_request_accounts.user_email, token)
                        if not user_info:
                            create_user(token, user_request_accounts.user_email, 'temp@123', user_request_accounts.first_name, user_request_accounts.last_name)
                            user_id = fetch_user_id_by_email(user_request_accounts.user_email, token)
                            ticket_url = generate_password_change_ticket(token, user_id, WEB_APP_URL)
                            change_password_email_data = EmailNotificationModel(
                            to=user_request_accounts.user_email,
                            subject="Password Reset Request for Your Account",
                            body=generate_email_html('reset', user_request_accounts.user_email, ticket_url))
                            send_email(change_password_email_data, request)
                    current_time = int(datetime.utcnow().timestamp())

                    logger.info(f"headers origin{Origin}")
                    if not Origin:
                        Origin = 'https://genaiot-dev.moschip-digitalsky.com'
                    temp_url=Origin
                    logger.info(f"{Origin},{temp_url}")

                    verify_link = f"{temp_url}/verifyUser/{user_account_id}/users"
                    logger.info(f"verify_link {verify_link}")
 
                    email_data = EmailNotificationModel(
                    to=user_request_accounts.user_email,
                    subject="User is Registered Successfully",
                    body=generate_email_html('verify', user_request_accounts.first_name, verify_link))
                    send_email(email_data, request)
                    logger.info(f"Email notification sent to {email_data} user_account_id-{user_account_id} rolesid-{user_request_accounts.user_roleid} account_types_id-{user_request_accounts.account_id}")
                    if "successfully" in result['msg']:
                        return {"status": True, "message": result}
                    else:
                        return {"status": False, "message": result}
                    
                    # if "successfully" not in result['msg']:
                    #     return {"status": True, "message": result}
                    
                    # else:
                    #     return {"status": False, "message": result}



                except Exception as e:
                    logger.error(f"Database insertion failed: {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to insert user accounts into the database.{e}",
                    )

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred. {e}",
        )

    

@router.get('/accounts/view_users', status_code=status.HTTP_200_OK,
            name="Get user user accounts by app_short_code and account id")
async def get_users(request: Request, account_id: Optional[UUID] = None, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            try:

                queryStr = f"SELECT roles.display_name as role_name, ua.* { ',acc.display_name as account_name, acc_cat.display_name as cat_name' if account_id == None else ''} FROM accounts.user_accounts as ua JOIN accounts.roles as roles on ua.user_roleid = roles.id { 'JOIN accounts.accounts as acc on acc.id = ua.account_id JOIN accounts.master_account_categories as acc_cat on acc_cat.id = acc.account_category_id' if account_id == None else '' }"
                tpl = [app_short_code]
                queryStr += """ WHERE ua.app_short_code = %s AND roles.display_name != 'Super Admin' """                
                if account_id is not None:
                    tpl.append(account_id)
                    queryStr += """ and ua.account_id=%s """
                
                queryStr += """ order by id"""
                
                await cur.execute(queryStr, tuple(tpl))
                results = await cur.fetchall()
                logger.info(results)
                if results:
                    return {"status": True, "message": "User founds with this account.","data": results}
                else:
                    return {"status": False, "message": "No user associated to this account."}
            
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An unexpected error occurred. {e}",
                )

@router.get('/verifyUser/{id}/{action}', status_code=status.HTTP_200_OK, name="Verify Accounts and users from email verify link")
async def verify_user_accounts(id: str, request: Request, action: str):
    try:
        table_map = {
            "accounts": "accounts.accounts",
            "users": "accounts.user_accounts"
        }
        statusOfUser = "status" if action == 'accounts' else "user_status"
        table = table_map[action]
        
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                # Fetch account details
                queryStr = f"SELECT * FROM {table} WHERE id = %s"
                await cur.execute(queryStr, (id,))
                results = await cur.fetchone()

                if results is None :
                    return {"status":False,"message": f"{action} not found", "data": results}
                    
                # logger.info(f"account found {results['verify_url_time']}{results}")
                # print(results["verify_url_time"])
                # print(statusOfUser)

                if results[statusOfUser] is True:
                    return {"status":False,"message": "Already Verified", f"{statusOfUser}": results[statusOfUser]}
                     

                current_time = int(datetime.utcnow().timestamp())
                time_difference = current_time - results['verify_url_time']
                
                if time_difference > 86400:
                    logger.info(f"link expired {time_difference}")
                    return {
                            "message": "Verification link expired",
                            "time_difference": time_difference,
                            "user_status": False }
                     
                
                # Update verification status
                queryStr = f"UPDATE {table} SET {statusOfUser} = TRUE WHERE id = %s returning {statusOfUser}"
                await cur.execute(queryStr, (id,))
                result = await cur.fetchone()
                
                if result:
                    return {"message": f"{action} verified successfully", f"{statusOfUser}": result[statusOfUser]}

                else:
                    return {"message": f"{action} not verified successfully", f"{statusOfUser}": False}  

    except Exception as e:
        logger.error(f"Error occurred during verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the verification request: {e}"
        )
