from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class UserRegistration(BaseModel):
  
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    age: Optional[int] = Field(default=None, ge=18, le=120)
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    # 3. Field validator for email lowercasing
    @field_validator("email")
    @classmethod
    def lower_email(cls, value: EmailStr) -> str:
        return value.lower()

    # 4. Field validator for username character set
    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        # Check alphanumeric + underscore only
        if not value.replace("_", "").isalnum():
            raise ValueError("Username must contain only letters, numbers, and underscores")
        return value

    # 5. Model validator (cross-field logic)
    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

    
user = UserRegistration(
    username="  john_doe99  ",
    email="JOHN@EXAMPLE.COM",
    age=25,
    password="supersecret123",
    confirm_password="supersecret123",
)

print(user.username)  
print(user.email)     