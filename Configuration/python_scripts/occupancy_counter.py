occupancy = 0
occupancy_other = 0

for entity_id in hass.states.get('group.occupancy').attributes['entity_id']:
    state = hass.states.get(entity_id)
    if state.state == 'on':
        occupancy = occupancy + 1
        
for entity_id in hass.states.get('group.occupancy_other').attributes['entity_id']:
    state = hass.states.get(entity_id)
    if state.state == 'on':
        occupancy_other = occupancy_other + 1

hass.states.set('counter.occupancy', occupancy, {
    'friendly_name': 'Occupancy Counter'
} )
hass.states.set('counter.occupancy_other', occupancy_other, {
    'friendly_name': 'Occupancy Other Counter'
} )