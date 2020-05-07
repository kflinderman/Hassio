wattHour = 0
cpuWhr = 0
totalWhr = 0
hueEntities = ['sensor.tripod_light_hours', 'sensor.rock_lamp_light_hours', 'sensor.floor_lamp_light_hours', 'sensor.chair_lamp_light_hours', 'sensor.swirl_lamp_light_hours', 'sensor.nursery_light_hours', 'sensor.front_door_light_hours', 'sensor.basement_1_light_hours', 'sensor.basement_2_light_hours', 'sensor.basement_3_light_hours', 'sensor.basement_4_light_hours', 'sensor.dining_room_light_hours', 'sensor.dining_room_light_hours', 'sensor.dining_room_light_hours', 'sensor.dining_room_light_hours', 'sensor.dining_room_light_hours', 'sensor.deck_light_hours', 'sensor.sewing_light_hours']
lightbulbEntities = ['sensor.sink_light_hours', 'sensor.basement_floor_light_hours', 'sensor.washroom_light_hours', 'sensor.bedroom_fan_hours', 'sensor.bedroom_fan_hours', 'sensor.nursery_fan_hours', 'sensor.nursery_fan_hours', 'sensor.nursery_fan_hours', 'sensor.craft_room_fan_hours', 'sensor.craft_room_fan_hours', 'sensor.craft_room_fan_hours', 'sensor.master_bathroom_hours', 'sensor.master_bathroom_hours', 'sensor.master_bathroom_hours']
compEntities = ['sensor.computer_hours']
ledEntities = ['sensor.cabinet_light_hours', 'sensor.cabinet_light_hours', 'sensor.cabinet_light_hours', 'sensor.guest_bedroom_fan_hours', 'sensor.guest_bedroom_fan_hours', 'sensor.guest_bedroom_fan_hours', 'sensor.guest_bedroom_fan_hours', 'sensor.guest_bedroom_fan_hours', 'sensor.basement_hallway_light_hours', 'sensor.upstairs_hallway_light_hours']
marketEntities = ['sensor.market_light_hours', 'sensor.sun_room_market_hours']
halogenEntities = ['sensor.entrance_light_hours', 'sensor.entrance_light_hours']

for entity_id in hueEntities:
  # copy it's state
  state = hass.states.get(entity_id)
  
  if state.state is not 'unknown':
     wattHour = wattHour + (int(float(state.state)) * 8.5)
	 
for entity_id in lightbulbEntities:
  # copy it's state
  state = hass.states.get(entity_id)
  
  if state.state is not 'unknown':
     wattHour = wattHour + (int(float(state.state)) * 60)
	 
for entity_id in ledEntities:
  # copy it's state
  state = hass.states.get(entity_id)
  
  if state.state is not 'unknown':
     wattHour = wattHour + (int(float(state.state)) * 20)
	 
for entity_id in marketEntities:
  # copy it's state
  state = hass.states.get(entity_id)
  
  if state.state is not 'unknown':
     wattHour = wattHour + (int(float(state.state)) * 110)
	 
for entity_id in halogenEntities:
  # copy it's state
  state = hass.states.get(entity_id)
  
  if state.state is not 'unknown':
     wattHour = wattHour + (int(float(state.state)) * 26)
     
for entity_id in compEntities:
  # copy it's state
  state = hass.states.get(entity_id)
  
  if state.state is not 'unknown':
     cpuWhr = cpuWhr + (int(float(state.state)) * 450)
     
totalWhr = wattHour + cpuWhr
totalWhr = round(totalWhr / 1000, 2)
wattHour = round(wattHour / 1000, 2)
cpuWhr = round(cpuWhr / 1000, 2)

hass.states.set('sensor.totalwhr', totalWhr, {
    'unit_of_measurement': 'kWh',
    'friendly_name': 'Daily Total Usage',
    'icon': 'mdi:power-socket-us'
})

hass.states.set('sensor.watthour', wattHour, {
    'unit_of_measurement': 'kWh',
    'friendly_name': 'Light Total Usage',
    'icon': 'mdi:power-socket-us'
})

hass.states.set('sensor.cpuwhr', cpuWhr, {
    'unit_of_measurement': 'kWh',
    'friendly_name': 'CPU Total Usage',
    'icon': 'mdi:power-socket-us'
})