# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s docent.hoa.rvspots -t test_rvspots.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src docent.hoa.rvspots.testing.DOCENT_HOA_RVSPOTS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_rvspots.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a RVSpots
  Given a logged-in site administrator
    and an add rvspots form
   When I type 'My RVSpots' into the title field
    and I submit the form
   Then a rvspots with the title 'My RVSpots' has been created

Scenario: As a site administrator I can view a RVSpots
  Given a logged-in site administrator
    and a rvspots 'My RVSpots'
   When I go to the rvspots view
   Then I can see the rvspots title 'My RVSpots'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add rvspots form
  Go To  ${PLONE_URL}/++add++RVSpots

a rvspots 'My RVSpots'
  Create content  type=RVSpots  id=my-rvspots  title=My RVSpots


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the rvspots view
  Go To  ${PLONE_URL}/my-rvspots
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a rvspots with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the rvspots title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
