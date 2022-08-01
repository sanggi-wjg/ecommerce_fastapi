from pydantic import BaseModel, PositiveInt


class AddressBase(BaseModel):
    id: PositiveInt


class AddressCreate(BaseModel):
    zipcode: str
    address_primary: str
    address_detail: str


class Address(AddressBase):
    zipcode: str
    address_primary: str
    address_detail: str

    class Config:
        orm_mode = True


class UserAddressBase(BaseModel):
    id: PositiveInt


class UserAddress(UserAddressBase):
    user_id: PositiveInt
    address_id: PositiveInt
    address: Address

    class Config:
        orm_mode = True
