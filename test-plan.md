Parkly Parking Management App - Test Plan
Testing Approach
What I chose to test and why
My exploration focused on three risk areas that matter most for a parking management system:

Business logic - Slot assignment and fee calculation are the core operations of a parking system. Errors here directly affect the service's reliability. 

Data privacy and authorization - Multi-user systems require clear boundaries between accounts. Without proper isolation, user data and actions can leak across accounts. 

Input validation - Parking systems depend on structured data (plate numbers, slot identifiers). Without enforced validation on both client and server, data integrity cannot be guaranteed. 

Visual and UX inconsistencies were identified but were considered lower priority compared to functional correctness, data integrity, and security-related flows.
How I structured my testing
I followed a risk-based approach:

Authentication - Verifying the login gateway and ensuring that internal pages are protected from unauthorized access. 
Core flows - testing the main parking lifecycle: start parking, end parking, and view history 
Boundary and negative testing - Challenging the system with duplicate entries, invalid formats, and concurrent session attempts. 
Data integrity - Validating that data submitted via the UI is stored and retrieved accurately from the database. 
Authorization - Testing data access to ensure users cannot view or modify data belonging to others.


Test Cases
Authentication
TC-01 - Login with valid credentials
Precondition: App running at localhost:5000, user admin / password exists
Steps: Navigate to login page, enter valid credentials, click Login
Expected: User is taken to the Dashboard
Result: PASS
TC-02 - Login with empty fields 
Precondition: On Login page
Steps: Leave username and/or password empty, click Login 
Expected: Submission is blocked and the user is prompted to fill in the missing field 
Result: PASS
TC-03 - Login with invalid credentials  
Precondition: On Login page
Steps: Enter invalid credentials (e.g. valid username with wrong password, or non-existing username), click Login  
Expected: Error message displayed immediately on the login page indicating that the credentials are incorrect  
Result: FAIL - password field clears silently with no feedback. Error messages appear on Dashboard only after a subsequent successful login. 
TC-04 - Forgot Password flow
Precondition: On Login page
Steps: Click "Forgot Password"
Expected: User is taken to a password reset page or shown instructions for account recovery
Result: FAIL - navigates to https://cataas.com (external cat image website)


Parking Logic
TC-05 - Start parking session with valid input
Precondition: Logged in, valid car plate available (8 digits, non-sequential)
Steps: Fill in Car Plate, Vehicle Type, Slot (e.g. slot 5), click Start Parking
Expected: Session starts and appears in the list of active sessions   
Result: PASS
TC-06 - End parking session and verify fee
Precondition: Active parking session exists
Steps: Click End Parking on an active session
Expected: Message shown that parking has ended and the fee amount (e.g. "Parking ended. Fee: 0.15")
Result: FAIL - message displays "Fee: 0.15 (חיוב: error)" which makes it unclear to the user whether payment was processed successfully. Fee does appear correctly in History.
TC-07 - Assign two vehicles to the same slot
Precondition: Vehicle A (e.g. plate 12345663) is actively parked in slot X (e.g. slot 12)
Steps: Start a new parking session for a different vehicle (e.g. plate 32323654) in the same slot X
Expected: System blocks the action with a message that the slot is already occupied
Result: FAIL - both sessions are created successfully, slot is double-booked
TC-08 - Duplicate car plate prevention
Precondition: A vehicle (e.g. plate 12345663) already has an active parking session
Steps: Try to start a new session for the same plate
Expected: System blocks the action
Result: PASS - system blocks with message "Duplicate parking prevented: this car is already parked." A vehicle cannot have two active sessions simultaneously.


Data and Authorization
TC-09 - Data isolation between users
Precondition: Two separate user accounts exist (User A and User B)
Steps: Login as User A, create a parking session. Logout. Login as User B, navigate to Dashboard.
Expected: User B sees only their own data. Active sessions created by User A should not be visible.
Result: FAIL - User B sees all parking sessions from all users with no indication of ownership. This applies to Dashboard, History, and all active sessions.
TC-10 - Input validation on Slot field
Precondition: On Dashboard, Start Parking form
Steps: Enter a long string of mixed characters including letters, and special characters in the Slot field, submit the form
Expected: Validation error - the field should have defined rules for accepted values
Result: FAIL - field accepts any input with no restriction. There is also no indication of which fields are required before attempting to submit.
TC-11 - Evidence of potential missing server-side validation 
Precondition: Logged in
Steps: Navigate to History page and observe existing records 
Expected: All car plates conform to 8-digit rule 
Result: FAIL - History contains records that violate client-side rules (e.g. dvdsvd, dor123, 21341243252465234645). This suggests that server-side validation may be missing or was not consistently enforced at some point. 


User Management
TC-12 - Delete user with no active sessions
Precondition: User exists and has completed parking sessions (no currently active session)
Steps: Login as admin, navigate to Users, click Delete on that user
Expected: User is deleted successfully. A user with no active sessions should be removable.
Result: FAIL - system blocks deletion with "Cannot delete user with parking sessions" even when no sessions are active. The behavior suggests that historical sessions are also considered, without clear indication to the user. As a result, users cannot be removed after having used the system. 
TC-13 - Access internal pages without a valid session
Precondition: No active login session (e.g. fresh browser with no prior login)
Steps: Navigate directly to localhost:5000/history via the address bar
Expected: User is taken to the Login page
Result: PASS - the system correctly requires an active session cookie. Accessing any internal URL without a valid session redirects to login.


Top 5 Significant Bugs
BUG-01 - Two Vehicles Can Occupy the Same Slot [Critical]
Impact: The system allows multiple vehicles to be assigned to the same parking slot at the same time. There is no backend validation enforcing slot uniqueness. This indicates missing validation for slot availability at the system level.

Steps to reproduce:

Login, start parking for vehicle A (e.g. plate 12345663) in slot X (e.g. slot 12)
Start parking for a different vehicle B (e.g. plate 32323654) in the same slot X

Expected: Second session blocked - slot already occupied
Actual: Both sessions created successfully, both appear as active


BUG-02 - All Users See All Data [Critical]
Impact: There is no separation between user accounts. Every logged-in user sees all parking sessions, all history, and all active slots regardless of who created them. There are no permission levels and no ownership indicators. The system behaves as if all users share one account.

Steps to reproduce:

Login as User A, create a parking session
Logout, login as User B
Check Dashboard and History

Expected: User B sees only their own data
Actual: User B sees all sessions from all users. There is no data isolation between accounts and no ownership indicators. All users, including admin, operate with identical access to all system data. 


BUG-03 - Forgot Password Navigates to External Cat Website [Critical]
Impact: Clicking "Forgot Password" takes the user to https://cataas.com, an unrelated external site (showing random cat images). There is no password reset functionality in the application. A user who is locked out of their account has no recovery path.

Steps to reproduce:

Navigate to the Login page
Click "Forgot Password"

Expected: User is taken to a password reset page or shown recovery instructions
Actual: Browser navigates to https://cataas.com


BUG-04 - End Parking Shows Error String Alongside Fee [High]
Impact: When ending a parking session, the system displays the message "Fee: 0.15 (חיוב: error)". The fee amount does appear correctly in History, but the error string shown at checkout makes it unclear 
to the user whether payment was processed successfully.


Steps to reproduce:

Start a parking session
Wait a few seconds
Click End Parking

Expected: "Parking ended. Fee: 0.15" - clear confirmation with no error messages
Actual: "Parking ended. Fee: 0.15 (חיוב: error)" 


BUG-05 - Users Cannot Be Deleted After Any Parking Activity [High]
Impact: The system blocks deletion of any user who has ever had a parking session, even after all sessions are fully closed. The error message "Cannot delete user with parking sessions" does not distinguish between active and historical sessions. This means users cannot be removed from the system by an admin, and users cannot delete their own accounts after having used the service.

Steps to reproduce:

Create a new user, start and fully end a parking session as that user
Login as admin, navigate to Users, click Delete on that user

Expected: User deleted successfully - no active sessions exist
Actual: Deletion blocked - system treats any historical session as a permanent block on deletion

