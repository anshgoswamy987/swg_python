from pydantic import BaseModel , Field , field_validator, model_validator, ConfigDict
from typing import Literal

class UserAccount (BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace= True,
        extra = "forbid"
    )

    account_id : str = Field(pattern=r"^USR-\d{5}$")
    username: str = Field(min_length = 4 , max_length=16)
    age: int = Field(ge=18, le=100)
    is_verified : bool = Field(default = False)
    tier : Literal["free","pro","enterprise"] = "free"

    @field_validator("username")
    @classmethod
    def _lowercase(cls,value:username)->str:
        return value.lower()

    @model_validator(mode="after")
    def validate_enterprise_tier(self):
        if self.tier == "enterprise" and not self.is_verified:
            raise ValueError("Enterprise tier accounts must be verified.")
        return self  

    # 1. Valid free user (username auto-lowercased)
user1 = UserAccount(
    account_id="USR-10293",
    username="AlexDev99",
    age=22,
)
print(user1.username)  # "alexdev99"
print(user1.tier)      # "free"

# 2. Enterprise without verification -> Raises ValidationError!
try:
    UserAccount(
        account_id="USR-99999",
        username="bigcorp",
        age=30,
        tier="enterprise",
        is_verified=False,
    )
except Exception as e:
    print("\nCaught expected error:\n", e)
