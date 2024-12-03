from typing import Any, Optional,List, Union, Dict
from fastapi import File, UploadFile
from pydantic import BaseModel, Field, validator, validator
import json
from uuid import uuid4, UUID


class Account_Types(BaseModel):
    # id: UUID = Field(default_factory=uuid4)
    id: int
    app_short_code: str
    display_name: str
    short_code: str
    account_category_display_name: str
    account_subcategory: str
    account_classification: str
    self_registration_allowed: bool
    parent_account_display_name: str | None = None

class Post_Account_Types(BaseModel):
    # id: UUID = Field(default_factory=uuid4)
        app_short_code: str
        display_name: str
        short_code: str
        account_category_id: int  
        account_subcategory:str      
        account_classification: str
        self_registration_allowed: bool
        parent_account_type_id: int   

class AccountsAddress(BaseModel):
    country: str
    state: str
    city: str
    addressline1: str
    addressline2: str
    zipcode: str

class AccountsContactDetails(BaseModel):
    contactname: str
    contactemail: str
    contactnumber: str

class Accounts(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    display_name: str
    account_type_id:int
    account_category_display_name: str
    account_type_display_name: str
    account_subcategory: str | None = None
    address: Optional[AccountsAddress]=None
    contactdetails: AccountsContactDetails
    logo_uri: str | None = None
    status: bool
    parent_id: None | UUID = Field(default_factory=uuid4)
    grandparent_id: None | UUID = Field(default_factory=uuid4) 

class MasterAccountCategories(BaseModel):
    id: int
    display_name: str

class MasterClaimsMicroservice(BaseModel):
    feature_name: str
    display_name: str
    name: str
    type: str
    is_default_claim: bool
    microservice_id: Optional[int]=None

class MasterClaims(BaseModel):
    id: int
    feature_name: str
    display_name: str
    name: str
    type: str
    is_default_claim: bool
    microservice_display_name: str

class MasterMicroServices(BaseModel):
    id: int
    display_name: str

class MasterPoliciesClaims(BaseModel):
  claims: list

class MasterPoliciesMenu(BaseModel):
    menu : Any | None = None

class MasterPolicies(BaseModel):
    id: int
    microservice_id: int
    microservice_display_name: str
    display_name: str
    claims: MasterPoliciesClaims
    menu: MasterPoliciesMenu | None = None
    permissions_required: bool

class MasterPoliciesRequest(BaseModel):
    microservice_id: int
    display_name: str
    claims: MasterPoliciesClaims
    menu: MasterPoliciesMenu | None = None
    permissions_required: bool

class RoleWisePoliciesAndPermissions(BaseModel):
    id: int
    app_short_code: str
    role_id: int
    policy_id: int
    policy_permissions: Any

class Roles(BaseModel):
    id: int
    app_short_code: str
    account_type_name: str
    display_name: str
    is_it_admin_role: bool

class UserAccounts(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    account_id: UUID = Field(default_factory=uuid4)
    app_short_code: str
    user_email: str
    user_login: str
    user_fullname: str
    user_mobile: str
    user_globalid: str
    user_roleid: int
    user_status: bool

# database table names for reference ....
#   (id, name, parent_account_id, category, type, adress_line_1, adress_line_2, contact_name, contact_email, contact_phone)
class Policy(BaseModel):
    mpid: Union[int, str, None]  
    name: str
    policyId: Optional[int]  
    rwppid: Optional[int]  
    role_id: Optional[int] 
    permission: Optional[Any]  

class MicroserviceResponse(BaseModel):
    msid: int
    name: str
    policies: Optional[List[Policy]]  

class Post_Account_Types(BaseModel):
    # id: UUID = Field(default_factory=uuid4)
        display_name: str
        short_code: str
        account_category_id: int  
        account_subcategory:str      
        account_classification: str
        self_registration_allowed: bool
        parent_account_type_id: Optional[int]=None   
class Post_Account_confriguations(BaseModel):
        is_site: bool|str=None
        is_fleet: bool|str=None
        is_super_asset: bool|str=None
class PostRoles(BaseModel):
    app_short_code: str
    account_type_id: str
    display_name: str
    is_it_admin_role: bool
class Put_Account_overview(BaseModel):
    description: str = None
    icon_uri: UploadFile | str | None = File(None, media_type="image/*")
    logo_uri: UploadFile | str | None = File(None, media_type="image/*")

class AccountTypesByCategory(BaseModel):
    name: str
    value: int

class CustomerAccounts(BaseModel):
    display_name: str
    account_category_id: int
    account_type_id: int
    address: Optional[AccountsAddress]=None
    contactdetails:AccountsContactDetails=None
    logo_uri: str | None = None
    parent_id:Optional [UUID]=None
    grandparent_id:Optional[UUID]=None

class AccountTypesByCategory(BaseModel):
    name: str
    value: int

class PartnerAccounts(BaseModel):
    display_name: str
    account_category_id: int
    account_type_id: int
    address: Optional[AccountsAddress]=None
    contactdetails:AccountsContactDetails=None
    logo_uri: str | None = None
    parent_id:Optional [UUID]=None
    grandparent_id:Optional[UUID]=None

class ServiceProviderAccounts(BaseModel):
    display_name: str
    account_category_id: int
    account_type_id: int
    address: Optional[AccountsAddress]=None
    contactdetails:AccountsContactDetails=None
    logo_uri: str | None = None
    parent_id:Optional [UUID]=None
    grandparent_id:Optional[UUID]=None
    
class SupportAccounts(BaseModel):
    display_name: str
    account_category_id: int
    account_type_id: int
    address: Optional[AccountsAddress]=None
    contactdetails:AccountsContactDetails=None
    logo_uri: str | None = None
    parent_id:Optional [UUID]=None
    grandparent_id:Optional[UUID]=None

class UpdateCustomerAccounts(BaseModel):
    display_name: str
    account_type_id: int
    address: Optional[AccountsAddress]=None
    contactdetails:AccountsContactDetails=None
    logo_uri: str | None = None
    grandparent_id:Optional[UUID]=None

class UpdatePartnerAccounts(BaseModel):
    display_name: str
    account_type_id: int
    address: Optional[AccountsAddress]=None
    contactdetails:AccountsContactDetails=None
    logo_uri: str | None = None
    grandparent_id:Optional[UUID]=None

class UpdateServiceProviderAccounts(BaseModel):
    display_name: str
    account_type_id: int
    address: Optional[AccountsAddress]=None
    contactdetails:AccountsContactDetails=None
    logo_uri: str | None = None
    grandparent_id:Optional[UUID]=None
    
class UpdateSupportAccounts(BaseModel):
    display_name: str
    account_type_id: int
    address: Optional[AccountsAddress]=None
    contactdetails:AccountsContactDetails=None
    logo_uri: str | None = None
    grandparent_id:Optional[UUID]=None
class MasterClaimsusingid(BaseModel):
    id: int
    feature_name: str
    display_name: str
    name: str
    type: str
    is_default_claim: bool
    microservice_id: int
    microservice_display_name:str


class UserRequestModel(BaseModel):
    account_id: str
    app_short_code: str
    user_email: str
    first_name: Optional[str] = None
    user_mobile: str
    user_roleid: int
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    user_fullname: Optional[str] = None
