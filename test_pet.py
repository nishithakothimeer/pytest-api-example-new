from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_


'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''

def test_pet_schema():
        pet_ids = [1,2] # In Swagger created pet I'd and retrieved it via Get request and validated the same in the following script.

        for pet_id in pet_ids: # Loop through each pet ID to test the retrieved and schema validation
            test_endpoint = f"/pets/{pet_id}"
            response = api_helpers.get_api_data(test_endpoint)

            assert response.status_code == 200, f"Expected 200 but got {response.status_code} for pet_id {pet_id}" #Verify the response code
            validate(instance=response.json(), schema=schemas.pet)
            print(response.text)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
@pytest.mark.parametrize("status", ["available", "sold", "pending",]) # Validation for the available statuses
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {"status": status}

    response = api_helpers.get_api_data(test_endpoint, params)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}" # to Verify the request was successful

    pets_list = response.json()
    for pet in pets_list:
        # Verify status matches expected
        assert pet["status"] == status, f"Expected {status} but got {pet['status']}"
        # Validate schema
        validate(instance=pet, schema=schemas.pet)


    print(response.text)


'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''


@pytest.mark.parametrize("pet_id", [-1,111,"2@","ab.c"])  # Tested with Invalid Test ID's
def test_get_by_id_404(pet_id):
    test_endpoint = f"/pets/{pet_id}"
    response = api_helpers.get_api_data(test_endpoint)
    # Verify that the response status code is 404 (Not Found) and print the actual status code
    assert response.status_code == 404, f"Expected 404, got {response.status_code}. Response: {response.text}"
    assert_that(response.text.upper(), contains_string(" NOT FOUND")) # to verify response body
    print(response.status_code)



