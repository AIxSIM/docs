import xmltodict

def parse_population_xml(file_path):
    """Parse Population.xml and map person IDs to their types and attributes."""
    with open(file_path, 'r', encoding='utf-8') as file:
        population_data = xmltodict.parse(file.read())

    person_mapping = {}

    # Traverse the XML structure
    categories = population_data['population']['personal_category']
    if isinstance(categories, dict):  # If there's only one category
        categories = [categories]

    for category in categories:
        roles = category.get('roles', {}).get('role', [])
        if isinstance(roles, dict):  # If there's only one role
            roles = [roles]

        for role in roles:
            role_id = role['@id']
            persons = role.get('person', [])
            if isinstance(persons, dict):  # If there's only one person
                persons = [persons]

            for person in persons:
                person_id = person['@id']
                person_mapping[person_id] = {
                    'type': role_id,
                    'name': person.get('name', None),
                    'attributes': person.get('attributes', {}).get('attribute', [])
                }

    return person_mapping

def parse_agent_xml(file_path, person_mapping):
    """Parse Agent.xml and map vehicles to their person attributes."""
    with open(file_path, 'r', encoding='utf-8') as file:
        agent_data = xmltodict.parse(file.read())

    vehicles = agent_data['routes']['vehicle']
    if isinstance(vehicles, dict):  # If there's only one vehicle
        vehicles = [vehicles]

    for vehicle in vehicles:
        person_id = None
        attributes = vehicle.get('attribute', [])
        
        if isinstance(attributes, dict):  # If there's only one attribute
            attributes = [attributes]

        for attribute in attributes:
            if attribute['@name'] == 'person_id':
                person_id = attribute['#text']
                break

        if person_id and person_id in person_mapping:
            print(f"Vehicle ID: {vehicle['@id']}")
            print(f"Person ID: {person_id}")
            print(f"Person Type: {person_mapping[person_id]['type']}")
            print(f"Person Name: {person_mapping[person_id].get('name', 'Unknown')}")
            print(f"Person Attributes: {person_mapping[person_id]['attributes']}")
        else:
            print(f"Vehicle ID: {vehicle['@id']} has no valid person mapping.")

# File paths for XML files
population_file_path = 'Population.xml'
agent_file_path = 'Agent.xml'

# Process Population.xml and create the mapping
person_mapping = parse_population_xml(population_file_path)

# Process Agent.xml and print vehicle-person mappings
parse_agent_xml(agent_file_path, person_mapping)

