# Requirement ID: FR_hybrid_1
- Description: The system shall display a distinct 'Premium' badge on all content requiring a paid subscription, visible during searches.
- Source Persona: [Budget Conscious Valerie]
- Traceability: [Derived from review group H1]
- Acceptance Criteria: [Given a user is browsing the meditation library, When they view the content list, Then all paid items must display a 'Premium' icon, and free items must remain unbadged.]
- Notes: [Refined from FR_auto_2 to ensure visual clarity and prevent the paywall frustration cited in the hybrid persona.]

# Requirement ID: FR_hybrid_2
- Description: The system shall send a push notification 48 hours before a 7-day free trial converts into a paid annual subscription.
- Source Persona: [Budget Conscious Valerie]
- Traceability: [Derived from review group H1]
- Acceptance Criteria: [Given a user has an active free trial, When the trial reaches the 5-day mark, Then the system must trigger a push notification with a direct link to the cancellation page.]
- Notes: [Improved from FR_auto_3 by adding specific timing and notification to address unexpected billing pain points.]

# Requirement ID: FR_hybrid_3
- Description: The system shall allow users to filter the Sleep Story library by specific narrator names.
- Source Persona: [Sleep Story Enthusiast Sam]
- Traceability: [Derived from review group H2]
- Acceptance Criteria: [Given a user is in the Sleep Stories section, When they select the 'Narrator' filter, Then the system must display an alphabetized list of available voices and update the library results upon selection.]
- Notes: [Developed from FR_auto_1 to address Sam's specific goal of finding narrator voices that ease anxiety.]

# Requirement ID: FR_hybrid_4
- Description: The system shall normalize audio volume across all sleep stories to a maximum peak of -12 dB to prevent sudden waking due to inconsistent recording levels.
- Source Persona: [Sleep Story Enthusiast Sam]
- Traceability: [Derived from review group H2]
- Acceptance Criteria: [Given a user plays any two different sleep stories, When the audio is analyzed, Then the peak volume difference between the tracks must not exceed 2 dB.]
- Notes: [New requirement created to address the inconsistent volume pain point identified in Sam's hybrid persona.]

# Requirement ID: FR_hybrid_5
- Description: The system shall continue audio playback without interruption when the device screen is locked.
- Source Persona: [Stability Prioritizing Ian]
- Traceability: [Derived from review group H3]
- Acceptance Criteria: [Given a meditation session is active, When the user presses the device lock button, Then the audio must continue to play without pausing or stuttering.]
- Notes: [Refined from vague stability claims in FR_auto_1 to address Ian's specific "audio stops when screen is off" pain point.]

# Requirement ID: FR_hybrid_6
- Description: The system shall provide a 'Support' dashboard where users can view the status of their open technical tickets.
- Source Persona: [Stability Prioritizing Ian]
- Traceability: [Derived from review group H3]
- Acceptance Criteria: [Given a user has submitted a bug report, When they access the 'My Tickets' section, Then they must see the current status (e.g., Pending, Investigating, Resolved) and the timestamp of the last agent response.]
- Notes: [Created to address the support ignore request feedback found in review group H3.]

# Requirement ID: FR_hybrid_7
- Description: The system shall refresh 'The Daily Calm' session at 12:00 AM local time every 24 hours with a unique audio track.
- Source Persona: [Routine Oriented Rachel]
- Traceability: [Derived from review group H4]
- Acceptance Criteria: [Given it is 12:01 AM, When a user opens the app, Then the 'Daily Calm' featured session must display a new title and content different from the previous 24-hour period.]
- Notes: [Refined from FR_auto_3 to ensure the habit-building routine cited in Rachel's persona is supported by daily content variety.]

# Requirement ID: FR_hybrid_8
- Description: The system shall allow users to add specific music tracks to a 'Morning Routine' widget on the app home screen.
- Source Persona: [Routine Oriented Rachel]
- Traceability: [Derived from review group H4]
- Acceptance Criteria: [Given a user is on the Home Screen, When they tap the 'Morning Routine' widget, Then the system must immediately begin playback of their pre selected daily session without further navigation.]
- Notes: [New requirement to address Rachel's constraint for one-tap access to her daily mindfulness routine.]

# Requirement ID: FR_hybrid_9
- Description: The system shall provide a 'Skip' button on all marketing prompts during the initial user onboarding flow.
- Source Persona: [Navigation Stressed Alex]
- Traceability: [Derived from review group H5]
- Acceptance Criteria: [Given a new user is in the onboarding flow, When a subscription deal is presented, Then a 'Skip' or 'Not Now' button must be visible without scrolling and be fully functional.]
- Notes: [Created to address the bombarded with deals feedback in H5 and Alex's need for a low stimulation entry into the app.]

# Requirement ID: FR_hybrid_10
- Description: The system shall allow subscribers to cancel their recurring payment within two clicks from the 'Account Settings' menu.
- Source Persona: [Navigation Stressed Alex]
- Traceability: [Derived from review group H5]
- Acceptance Criteria: [Given a user is in 'Account Settings', When they tap 'Manage Subscription' and then 'Cancel', Then the system must process the cancellation request immediately and provide a confirmation code.]
- Notes: [Refined from FR_auto_1 to specify a maximum click-path, addressing the challenging to cancel complaint in review group H5.]