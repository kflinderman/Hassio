residents = "group.residents"
known_occupancy = {
      "name": "Nursery", 
      "entity_id": "group.nursery", 
      "sensor": "binary_sensor.nursery_occupancy"
  }, {
      "name": "Living Room", 
      "entity_id": "group.livingroom", 
      "sensor": "binary_sensor.living_room_bay_occupancy"
  }, {
      "name": "Kitchen", 
      "entity_id": "group.kitchen", 
      "sensor": "binary_sensor.kitchen_occupancy"
  }, {
      "name": "Bedroom", 
      "entity_id": "group.bedroom", 
      "sensor": "binary_sensor.bedroom_occupancy"
  }, {
      "name": "Basement", 
      "entity_id": "group.basement_no_aux", 
      "sensor": "binary_sensor.basement_bay_occupancy"
  }

other_occupancy = {
      "name": "Craft Room", 
      "entity_id": "group.craft", 
      "sensor": "binary_sensor.craft_occupancy"
  }, {
      "name": "Guest Room", 
      "entity_id": "group.guest", 
      "sensor": "binary_sensor.guest_occupancy"
  }, {
      "name": "Sun Room", 
      "entity_id": "group.sun_room", 
      "sensor": "binary_sensor.sunroom_occupancy"
  }, {
      "name": "Dining Room", 
      "entity_id": "group.dining_room", 
      "sensor": "binary_sensor.dining_occupancy"
  }
log_enabled = "true"








def log_info(logger, data, msg):
  # log_enabled = str(data.get("log_enabled", "false"))
  if log_enabled.lower() == "true":
    logger.error(msg)


def log_error(logger, msg):
  logger.error(msg)
  # Notify the error via persistent_notification
  domain = "persistent_notification"
  service = "create"
  service_data = {}
  service_data["notification_id"] = "occupancy_error"
  service_data["title"] = "\U000026A0 occupancy error"
  service_data["message"] = "{}".format(msg)
  hass.services.call(domain, service, service_data, False)

def time_calculator(entity, date_now, time_now):
  time_capture = []
  date_capture = []
  date_time = []

  # Grab the time data
  state_change = hass.states.get(entity).last_changed
  date_time = str(state_change).split()
  date_capture = date_time[0].split('-')
  time_capture = date_time[1].split(':')
  time_capture[0] = (60 * int(time_capture[0])) + int(time_capture[1])

  # Check if the last used was over a day ago
  # This isn't great for midnight, but it's a trade off I'm willing to take
  log_info(logger, data, "Python Script: {} -> check {} for used today: {}".format(script_name, entity, int(date_now[2]) - int(date_capture[2])))
  if int(date_now[2]) - int(date_capture[2]) == 0:

    # Now return what the time difference is
    log_info(logger, data, "Python Script: {} -> check {} for used recently: {} minutes".format(script_name, entity, time_now[0] - time_capture[0]))
    return time_now[0] - time_capture[0]

  else:
    return 60

try:

  # Begin Information Sensor Setup
  script_name = "occupancy.py"
  attributes = {
        'friendly_name': 'Occupancy Data',
        'icon': 'mdi:account-group',
        'number_home': 0,
        'known_occupancy': 0,
        'other_occupancy': 0,
        'difference': 0
    }
  sensor_state = "Error"

  # Log start of execution
  log_info(logger, data, "Python Script: {} -> START of execution".format(script_name))

  # Grab the residents group
  # residents = data.get("residents", "")
  log_info(logger, data, "Python Script: {} -> residents group: {}".format(script_name, residents))

  if residents == "":
    # Error nothing there
    log_error(logger, "**Required parameter 'residents' is missing.**\n\nScript NOT executed.")
  else:
    # Now check to see who is home and count that number as total people that can occupy a room
    for entity_id in hass.states.get(residents).attributes['entity_id']:
      state = hass.states.get(entity_id)
      if state.state == 'home':
        attributes['number_home'] = attributes['number_home'] + 1

    # Grab the rooms
    # known_occupancy = data.get("known_occupancy", "")
    # other_occupancy = data.get("other_occupancy", "")

    if known_occupancy == "":
      # Error nothing there
      log_error(logger, "**Required parameter 'known_occupancy' is missing.**\n\nScript NOT executed.")
    elif other_occupancy == "":
      # Error nothing there
      log_error(logger, "**Required parameter 'other_occupancy' is missing.**\n\nScript NOT executed.")

    else:
      # Check every known room for occupancy and add it to the total known
      for entity_id in known_occupancy:
        state = hass.states.get(entity_id['sensor'])
        if state.state == 'on':
          attributes['known_occupancy'] = attributes['known_occupancy'] + 1

      # Check every unknown room for occupancy and add it to the total unknown
      for entity_id in other_occupancy:
        state = hass.states.get(entity_id['sensor'])
        if state.state == 'on':
          attributes['other_occupancy'] = attributes['other_occupancy'] + 1

      # Grab the difference, if it's + then there are less rooms occupied then people, if it's - then there are too many rooms occupied
      attributes['difference'] = attributes['number_home'] - (attributes['known_occupancy'] + attributes['other_occupancy'])
      if attributes['difference'] >= 0:
        sensor_state = "Working"

      else:
        # We will need time data to know when last the occupied rooms were influenced
        date_now = []
        time_now = []

        # Get the current time/date
        date_sensor = hass.states.get('sensor.date')
        date_now = str(date_sensor.state).split('-')
        time_sensor = hass.states.get('sensor.time')
        time_now = str(time_sensor.state).split(':')

        if int(time_now[0]) >= 20:
          date_now[2] = int(date_now[2]) + 1
          time_now[0] = (60 * (int(time_now[0]) - 20)) + int(time_now[1])
        else:
          time_now[0] = (60 * (int(time_now[0]) + 4)) + int(time_now[1])
        
        # If there are more known rooms that are occupied then people then we know all of the unknown ones should be off
        if attributes['known_occupancy'] >= attributes['number_home']:
          log_info(logger, data, "Python Script: {} -> known occupancy contains all residents".format(script_name))
          long_term_known = 0
          
          # See if the known occupancy is new. Could just be passing through
          for entity_id in known_occupancy:
            state = hass.states.get(entity_id['sensor'])
            if state.state == 'on':
              if time_calculator(entity_id['sensor'], date_now, time_now) >= 5:
                long_term_known = long_term_known + 1

          log_info(logger, data, "Python Script: {} -> long term known occupancy: {}".format(script_name, long_term_known))
          if long_term_known >= attributes['number_home']:

            # But there are unknown rooms that state they are occupied
            if attributes['other_occupancy'] > 0:
              log_info(logger, data, "Python Script: {} -> other occupancy are on".format(script_name))
              for entity_id in other_occupancy:
                state = hass.states.get(entity_id['entity_id'])
                if state.state == 'on':
                  if time_calculator(entity_id['entity_id'], date_now, time_now) >= 20:
                      log_info(logger, data, "Python Script: {} -> turn off: {}".format(script_name, entity_id['name']))
                      hass.services.call('homeassistant', 'turn_off', service_data={ 'entity_id': entity_id['entity_id'] })
              sensor_state = "Working"
          else:
            sensor_state = "Working"

        # There are less known rooms then the residents, time for a bit more checking
        else:

          # OK What I want to do here is grab all of the unknowns and only keep on the number of rooms that equals the number of residents . These rooms should have been on closest to the buffer without going under.
          # There are more rooms than people. We need to grab what we think are the actual occupied rooms
          if attributes['other_occupancy'] > attributes['number_home']:
            log_info(logger, data, "Python Script: {} -> other occupancy are on".format(script_name))
            time_compare = []
            for entity_id in other_occupancy:
              state = hass.states.get(entity_id['sensor'])
              if state.state == 'on':
                temp_compare = []
                temp_compare.append(entity_id['entity_id'])
                temp_compare.append(time_calculator(entity_id['entity_id'], date_now, time_now))
                
                time_compare.append(temp_compare)

            log_info(logger, data, "Python Script: {} -> rooms to check: {}".format(script_name, time_compare))
            occupancy_keep = [None] * attributes['number_home']

            for rooms in time_compare:

              log_info(logger, data, "Python Script: {} -> {} on for: {}".format(script_name, rooms[0], rooms[1]))
              # First we need to see if it's been occupied for longer than 15 min
              if rooms[1] >= 0:
                log_info(logger, data, "Python Script: {} -> spaces: {}".format(script_name, occupancy_keep))

                # Then we need to check to see if there are any empty spaces
                for x in range(len(occupancy_keep)):
                  log_info(logger, data, "Python Script: {} -> current looking at: {}".format(script_name, occupancy_keep[x]))
                  if occupancy_keep[x] == None:
                    occupancy_keep[x] = rooms
                    log_info(logger, data, "Python Script: {} -> after: {}".format(script_name, occupancy_keep[x]))
                    log_info(logger, data, "Python Script: {} -> spaces v2: {}".format(script_name, occupancy_keep))
                    break

                  # Otherwise compare to the room that's loaded and compare
                  else:
                    log_info(logger, data, "Python Script: {} -> new {}: {} vs current {}: {}".format(script_name, rooms[0], rooms[1], occupancy_keep[x][0], occupancy_keep[x][1]))
                    if rooms[1] < occupancy_keep[x][1]:

                      # It now needs to replace the old one and iterate
                      log_info(logger, data, "Python Script: {} -> before rotate: ".format(script_name, occupancy_keep[x]))
                      # it's showing nothing...
                      occupancy_keep.rotate(1)
                      log_info(logger, data, "Python Script: {} -> rotate: ".format(script_name, occupancy_keep))
                      occupancy_keep[x] = rooms
                      break

            sensor_state = "Working"

          # There are more people than rooms occupied, so we're done here
          else:
            log_info(logger, data, "Python Script: {} -> other occupancy are off".format(script_name))
            sensor_state = "Working"

  hass.states.set('sensor.occupy', sensor_state, attributes)

  #Log end action execution
  log_info(logger, data, "Python Script: {} -> END of execution".format(script_name))

except Exception as e:
  log_error(logger, "**An unhandled error has occurred.**\n\n{}".format(e))