from jsonschema import validate
import pytest
import schemas
import api_helpers
import uuid
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

# Fixture to create a pet with a unique ID and "available" status
# 1. Create pet
@pytest.fixture
def create_pet_and_order():
    # To  Generate a unique 7-digit integer to use as pet_id for test data
    pet_id =  pet_id = int(str(uuid.uuid4().int)[:7])

    # 1. Create pet
    response = api_helpers.post_api_data("/pets/", {
        "id": pet_id,
        "name": f"pet_{pet_id}",
        "type": "fish",
        "status": "available"
    })
    print("POST /pets/ status:", response.status_code, response.text)
    assert response.status_code in (200, 201)  # to verify success creation

    # 2. Confirm pet exists
    response = api_helpers.get_api_data(f"/pets/{pet_id}")
    print("GET /pets/{pet_id} status:", response.status_code, response.text)
    assert response.status_code == 200

    # 3. Create order
    order_response = api_helpers.post_api_data("/store/order", {"pet_id": pet_id})
    print("POST /store/order status:", order_response.status_code, order_response.text)
    assert order_response.status_code == 201

    return order_response.json()["id"]



# Valid status
@pytest.mark.parametrize("new_status", ["sold", "available", "pending",])
def test_patch_order_by_id(create_pet_and_order, new_status):
    order_id = create_pet_and_order # Get the order ID created
    patch_data = {"status": new_status}

    response = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_data) # send patch request to update the status
    assert response.status_code == 200, f"Update order failed with status {response.status_code}" # to verify the update was successful

    resp_json = response.json()
    assert resp_json.get("message") == "Order and pet status updated successfully" # verify response message

    if "order" in resp_json:
        validate(instance=resp_json["order"], schema=schemas.order_response) # Schema validation

    print(response.text)

#invalid status
@pytest.mark.parametrize("new_status", ["invalid_status", "", "123", None])
def test_patch_order_by_id_invalid_status(create_pet_and_order, new_status):
    order_id = create_pet_and_order
    patch_data = {"status": new_status}

    response = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_data)
    assert response.status_code == 400, f"Expected 400 for invalid status, got {response.status_code}"

    resp_json = response.json()
    assert "Invalid status" in resp_json.get("message", ""), "Expected invalid status error message"

    print(response.text)




