# Rules and Patterns of the API testing
- [Functions of Tourmanique API](#api_func)
- [Main rules](#main_rules)
  - [Frameworks and tools](#frameworks)
  - [Testing methodology](#methodology)
  - [Developers responsibilities](#dev_responsibilities)
- [The life cycle of a feature](#feature_life)
- [Unit testing](#unit)
- [Integration testing](#integration)
  - [Fixtures and cleaning up the database for the tests](#fixtures)
- [What do we test in the first place?](#must_test)
- [How to validate the API contract](#api_contract)
- [Steps of API testing](#api_steps)
- [What HTTP status codes we expect in response?](#status_codes)
- [Backend testing guide and examples](#guide)
  - [Where do we store the tests?](#tests_location)
  - [What does a typical test case and its code look like?](#tests_example)
- [All the HTTP status codes in details for better testing](#status_codes_details)
- [Executing Tests](#execute)

## Functions of Tourmanique API <a name="api_func"></a> 
- Backend\
Main API (REST) service for executing CRUD operations and (managing all the actions of it's services) takes a role of the bridge between each ML model services\
Functions:
    - receive photos from the user
    - write photo to S3 storage
    - send photos for processing
    - records information about the photo in the database
    - request processing results from Result Service


## Main rules <a name="main_rules"></a> 

### Frameworks and tools<a name="frameworks"></a> 
Testing frameworks must be configured:
-  ```PyTest``` for Unit, Integration Testing. 

Tools:
- ```Postman``` for sending requests and testing the API
- ```Docker``` for the ability to build and deploy the project 

### Testing methodology<a name="methodology"></a> 
Tests will be written only by **TDD (Test Driven Development)** methodology.\
Details are prescribed in the [**Main Tourmanique Test Strategy**](https://github.com/TourmalineCore/tourmanique-documentation#readme) \
This is a must-read if you're not already familiar with it

### Developers responsibilities<a name="dev_responsibilities"></a> 
Developers should:
1. Write the structured and detailed description of the contract scheme of the endpoints in the task cards to allow QA's to perform transparent API testing
2. Follow ```TDD```

## The life cycle of a feature<a name="feature_life"></a> 
The life cycle of a feature whether backend or frontend in the project "Tourmanique" is described in the [**Main Tourmanique Test Strategy**](https://github.com/TourmalineCore/tourmanique-documentation#readme) \
This is a must-read if you're not already familiar with it

## Unit testing<a name="unit"></a> 
- Unit tests will be writing using PyTest framework
- Developers are covering every method and module by unit tests where they should check the HTTP response status-code and the main functionality of the module

## Integration testing<a name="integration"></a> 
- Integration tests imply interaction with databases - at this stage ***it is obligatory to use a separate test database*** ```"test_db"``` (the main database - ```"tourmanique"```) for the next points:
  - Maintain atomicity of testing, where each test is independent of the other 
  - Optimization by avoiding overloading the main database with unnecessary test information

### Fixtures and cleaning up the database for the tests<a name="fixtures"></a> 
To comply with these extremely important points described above - ***you need to ensure that the database is cleaned after filling it after each test***
For example, you can implement it through ```pytest fixtures``` - functions executed by pytest before (and sometimes after) the actual test functions. The code in the fixture can do whatever you need it to do.
***In our fixtures will be written the logic of clearing the database before each test.***\
\
[***Click here*** to view some examples of the fixtures using and read more detailed information about them to succesfully implement them in the tests.](https://docs.pytest.org/en/stable/explanation/fixtures.html)


## What do we test in the first place?<a name="must_test"></a> 
To ensure the quality of the API by testing it, first of all, it is worth paying attention to the fact that
- User data is secure
  - Test request scenarios to any endpoint without a JWT token 
  - Test request scenarios to foreign endpoint with id by accessing the exact id of foreign endpoint (compare JWT tokens of users)
- [Observed unanimity of the API interaction contract (click for the details)](#api_contract)
  - The scheme of the request body corresponds to the actual one
  - The status codes in the request response match the pre-agreed ones

## How to validate the API contract <a name="api_contract"></a> 
Testing the contract schema and code statuses in API responses is a crucial step to ensure the proper functionality of an application. Here are some best practices to follow:

1. Use a tool such as Postman to send requests to the API and verify the responses. This tool allows you to easily test different scenarios and see the results of each request.

2. Verify that the response matches the defined contract schema. The contract schema defines the expected structure of the response, including the keys, values, and data types. 

3. Check the response code to ensure that it matches the expected behavior. For example, if a user is trying to access a resource that they do not have permission for, the response code should be **403 "FORBIDDEN".** 

4. Verify that the response body includes the expected data and that the data is valid. For example, if the API is returning user information, ensure that the data is accurate and up-to-date.

5. Repeat the testing process for different scenarios, such as error cases and edge cases.

By following these best practices, you can ensure that your API is properly tested and meets the expected functionality and behavior.

## Steps of API testing<a name="api_steps"></a> 

- Each test consists of individual test steps, which are atomic actions that the test must perform in each API testing thread.
- For each API request, the test must perform the following actions:
  - [**Check the correctness of the HTTP status code.**](#status_codes) For example, creating a resource should return ```201 CREATED```, while forbidden requests should return ```403 FORBIDDEN```, etc.
  - **Verify the usefulness of the response payload.** Check the correctness of the JSON body, names, types, and values of the response fields, including those in response to erroneous requests.
  - **Check the response headers.** HTTP server headers affect both security and performance.
  - **Verify the correctness of the application state.** This is optional and is mainly used for manual testing or when the user interface or other interface can be easily checked.
  - **Test the basic functionality.** If the operation was successfully completed but took an unreasonably long time, the test is not passed.


## What HTTP status codes we expect in response? <a name="status_codes"></a> 

In general, the status codes of API endpoints of the Tourmanique project:
- for positive scenarios - **200, 201**
- failed securiti scenarios - **401, 422**
- negative scenarios with errors in the contract scheme - **400, 500** 

## Backend testing guide and examples
<a name="guide"></a> 

### Where do we store the tests?<a name="tests_location"></a> 
In our project, the tests of the backend part are stored in the folder: ```tourmanique-api/tourmanique/tests/{*page_name*}``` and their name is typed with an underscore with ***test*** in the beginning:\
```tourmanique-api/tourmanique/tests/{*page_name*}/test_{*page_name*}.py```
For example, the ***test path of the authentication page*** is here: 
```tourmanique-api/tourmanique/tests/auth/test_auth.py``` \
The tests folder contains inside folders whose names tell you the specific pages.

### What does a typical test case and its code look like? <a name="tests_example"></a> 
1. For example, here's a test that checks the response status code for an attempt to create a gallery with an empty authentication token
```
def test_add_gallery_with_empty_token(flask_app):
    headers = {
        "Authorization": f"Bearer ''"
    }

    data = {
        'name': 'Test Gallery3',
    }
```
- In the body of the function, be sure to declare the request header and pass in the authentication value by pattern
- In the function body declare the variable data and declare there all the variables according to the contract scheme for the endpoint, pass valid values to the variables to comply with the atomicity principle (in this test case we manipulate only with the request header)


2. Then we declare a ```response``` variable and set a request method using a **flask**, passing in our ```data``` (in **json** format) and ```headers```
And then we use ```assert``` to make sure that the status code of the server's response really is ***UNPROCESSABLE ENTITY***
```
response = flask_app.post(url_for('api.galleries.add_gallery'), json=data, headers=headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
```
3. And there is full version of the test function:
```
def test_add_gallery_with_empty_token(flask_app):
    headers = {
        "Authorization": f"Bearer ''"
    }

    data = {
        'name': 'Test Gallery3',
    }

    response = flask_app.post(url_for('api.galleries.add_gallery'), json=data, headers=headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
```


## All the HTTP status codes in details for better testing<a name="status_codes_details"></a> 
Below are the endpoints and status codes for each scenario for those who were not particularly involved in development and for quality testing on the specification and response status code requirements


- ```Authenication endpoint```
  - Successfully authenticated - **200 "OK"** 
  - Wrong or empty credentials - **401 "UNAUTHORIZED"** 
  - Wrong request body (wrong or empty values of variables) - **400 "BAD REQUEST"**

- ```Gallery creating Endpoint```
  - Succesfully created - **201 "CREATED"**
  - Attempt to create a gallery with an empty name - **500 "INTERNAL SERVER ERROR"**
  - Attempt to create a gallery without JWT token - **401 "UNAUTHORIZED"**
  - Attempt to create a gallery with foreign JWT token - **422 "UNPROCESSABLE ENTITY"**
  - Attempt to create a gallery with wrong request body (wrong or empty values of variables) - **400 "BAD REQUEST"**
  - Attempt to create a gallery with wrong request body (wrong or empty variables) - **500 "INTERNAL SERVER ERROR"**

- ```Gallery renaming endpoint```
  - Succesfully renamed - **200 "OK"**
  - Attempt to rename a gallery to an empty name - **500 "INTERNAL SERVER ERROR"**
  - Attempt to rename a gallery without JWT token - **401 "UNAUTHORIZED"**
  - Attempt to rename a gallery with foreign JWT token - **422 "UNPROCESSABLE ENTITY"**
  - Attempt to rename a gallery with wrong request body (wrong or empty values of variables) - **400 "BAD REQUEST"**
  - Attempt to rename a gallery with wrong request body (wrong or empty variables) - **500 "INTERNAL SERVER ERROR"**

- ```Gallery deleting endpoint```
  - Succesfully deleted - **200 "OK"**
  - Attempt to delete a gallery if it's already deleted - **404 "NOT FOUND"**
  - Attempt to delete a gallery without JWT token - **401 "UNAUTHORIZED"**
  - Attempt to delete a gallery with foreign JWT token - **422 "UNPROCESSABLE ENTITY"**


- ```Galleries getting endpoint```
  - Succesfully got - **200 "OK"**
  - Attempt to get a galleries if it's already deleted - **404 "NOT FOUND"**
  - Attempt to get a galleries without JWT token - **401 "UNAUTHORIZED"**
  - Attempt to get a galleries with foreign JWT token - **422 "UNPROCESSABLE ENTITY"**
  

- ```Gallery photos getting endpoint```
  - Succesfully got - **200 "OK"**
  - Attempt to get a photos without JWT token - **401 "UNAUTHORIZED"**
  - Attempt to get a photos with foreign JWT token - **422 "UNPROCESSABLE ENTITY"**


- ```Gallery restoring endpoint```
  - Succesfully restored - **200 "OK"**
  - Attempt to restore a gallery without JWT token - **401 "UNAUTHORIZED"**
  - Attempt to restore a gallery with foreign JWT token - **422 "UNPROCESSABLE ENTITY"**
 

- ```Uploading a photo endpoint```
  - Succesfully uploaded (including 1x1px and 3000x3000px photos in JPEG, PNG file format) - **200 "OK"**
  - Attempt to upload a photo without JWT token - **401 "UNAUTHORIZED"**
  - Attempt to upload a photo with foreign JWT token - **422 "UNPROCESSABLE ENTITY"**
  - Attempt to upload a photo with wrong (wrong file format) or empty body - **500 "INTERNAL SERVER ERROR"**
  

## Executing Tests <a name="execute"></a> 
To execute Cypress component test, run this command in the terminal:
To execute PyTest tests and raise the test database, run this command in the terminal
```
make test
```
If you want to execute integration tests, run this command in the terminal:
```
make test --integration
```

