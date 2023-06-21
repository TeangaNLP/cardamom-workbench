Feature: User Sign Up
  Scenario: Validating user sign up with matching passwords and valid username and password
      Given a user is on the sign up page
      When the user clicks the sign up button
      And the password and confirmPassword match
      And the username is valid
      And the password is valid
      Then a request is sent to the API
