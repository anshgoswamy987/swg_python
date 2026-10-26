from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class CartItem(BaseModel):
    sku: str = Field(pattern=r"^ITEM-\d{4,}$")
    title: str = Field(min_length=2, max_length=60)
    unit_price: float = Field(gt=0.0)
    quantity: int = Field(gt=0)


class ShoppingCart(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    cart_id: str = Field(pattern=r"^CART-[A-Za-z0-9]{6}$")
    items: list[CartItem] = Field(min_length=1)
    tax_rate: float = Field(default=0.05, ge=0.0, le=0.30)
    total_cost: float = Field(gt=0.0)

    @field_validator("items")
    @classmethod
    def check_unique_skus(cls, items: list[CartItem]) -> list[CartItem]:
        # Extract all SKUs into a list
        skus = [item.sku for item in items]
        if len(skus) != len(set(skus)):
            raise ValueError("Duplicate SKUs detected in cart")
        return items

    @model_validator(mode="after")
    def verify_total_cost(self):
        # 1. Sum up: unit_price * quantity for every item
        subtotal = sum(item.unit_price * item.quantity for item in self.items)
        
        # 2. Add tax
        expected_total = subtotal * (1 + self.tax_rate)

        # 3. Guard against floating-point drift: compare rounded to 2 decimal places
        if round(self.total_cost, 2) != round(expected_total, 2):
            raise ValueError(
                f"total_cost mismatch: expected {round(expected_total, 2)}, "
                f"got {self.total_cost}"
            )
        return self


# ==========================================
# Quick Test Verification
# ==========================================
if __name__ == "__main__":
    # Test 1: Valid Cart
    # Subtotal: (2 * 10.0) + (1 * 5.0) = 25.0
    # Tax: 25.0 * 1.05 = 26.25
    cart = ShoppingCart(
        cart_id="CART-ABC123",
        items=[
            CartItem(sku="ITEM-1001", title="Mechanical Keyboard", unit_price=10.0, quantity=2),
            CartItem(sku="ITEM-1002", title="Mousepad", unit_price=5.0, quantity=1),
        ],
        tax_rate=0.05,
        total_cost=26.25,
    )
    print("Success! Cart created with ID:", cart.cart_id)
    print("Items count:", len(cart.items))