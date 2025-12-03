import xml.etree.ElementTree as ET
import random
import os

# 파일 경로 및 생성할 파일 개수를 설정
input_xml_file = 'C:/Users/yoomi/Desktop/internship/IITP/result/population_2.xml'
number_of_files_to_create = 100

# Step 1: 저장할 폴더 경로를 설정
output_directory = 'C:/Users/yoomi/Desktop/internship/IITP/agent_2'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Step 2: Read the XML file and get the total population
try:
    tree = ET.parse(input_xml_file)
    root = tree.getroot()
    total_population_text = root.find('text').find('total_population').text
    new_total_population = int(total_population_text)
except FileNotFoundError:
    print(f"오류: '{input_xml_file}' 파일을 찾을 수 없습니다. 파일 경로를 다시 확인해주세요.")
    exit()
except AttributeError:
    print("오류: XML 파일 구조가 예상과 다릅니다. 'text' 또는 'total_population' 태그를 찾을 수 없습니다.")
    exit()

# Step 3: Extract personal categories with min/max proportions
personal_categories_min_max = {}
for category in root.findall('personal'):
    personal_id = category.find('personal_job').text
    min_prop = float(category.find('personal_min').text)
    max_prop = float(category.find('personal_max').text)
    personal_categories_min_max[personal_id] = {'min': min_prop, 'max': max_prop}

# Step 4: Extract unified behavior categories
behavior_categories = {}
for category in root.findall('behavior'):
    name = category.find('behavior_name').text
    min_prop = float(category.find('behavior_min').text)
    max_prop = float(category.find('behavior_max').text)
    behavior_categories[name] = {'min': min_prop, 'max': max_prop}

# Step 5: Extract injured proportions
injury_min = float(root.find('injury').find('injury_min').text)
injury_max = float(root.find('injury').find('injury_max').text)

# Step 6: Identify rescuers
rescuers = ['medical workers', 'fire officer', 'police officer', 'bus driver', 'nuclear power plant worker']

# Main loop to create multiple files
for file_index in range(1, number_of_files_to_create + 1):
    output_xml_file = os.path.join(output_directory, f'agent_file_{file_index}.xml')

    # Step 7: Generate and normalize personal proportions for this file
    random_proportions = {}
    for personal_id, props in personal_categories_min_max.items():
        random_proportions[personal_id] = random.uniform(props['min'], props['max'])
    
    total_proportions_sum = sum(random_proportions.values())
    
    personal_categories = {}
    for personal_id, prop_val in random_proportions.items():
        personal_categories[personal_id] = prop_val / total_proportions_sum
    
    # Step 8: Calculate the number of people for each personal category
    calculated_agents = {}
    for personal_id, proportion in personal_categories.items():
        calculated_agents[personal_id] = round(new_total_population * proportion)

    # Adjust for rounding errors
    current_total = sum(calculated_agents.values())
    diff = new_total_population - current_total
    if diff != 0:
        if 'citizen' in calculated_agents:
            calculated_agents['citizen'] += diff
        else:
            first_key = list(calculated_agents.keys())[0]
            calculated_agents[first_key] += diff
    
    # Step 9: Generate agents list with their roles
    agents = []
    agent_id_counter = 1
    for personal_id, count in calculated_agents.items():
        is_rescuer = personal_id in rescuers
        for _ in range(count):
            agent_data = {
                'id': f'agent_{agent_id_counter}',
                'personal_id': personal_id,
                'is_rescuer': is_rescuer
            }
            agents.append(agent_data)
            agent_id_counter += 1
            
    # Step 10: Assign traits to ALL agents based on total population
    total_agents = len(agents)

    # Assign behavior traits
    for name, props in behavior_categories.items():
        min_prop, max_prop = props['min'], props['max']
        low_prop = random.uniform(min_prop, max_prop)
        num_low = round(total_agents * low_prop)
        
        all_agent_indices = list(range(total_agents))
        random.shuffle(all_agent_indices)
        
        for i, agent_idx in enumerate(all_agent_indices):
            level = 'low' if i < num_low else 'high'
            agents[agent_idx][name] = level

    # Assign injury trait
    injured_prop = random.uniform(injury_min, injury_max)
    num_injured = round(total_agents * injured_prop)
    
    all_agent_indices = list(range(total_agents))
    random.shuffle(all_agent_indices)
    for i, agent_idx in enumerate(all_agent_indices):
        level = 'injured' if i < num_injured else 'uninjured'
        agents[agent_idx]['injury'] = level
    
    # Step 11: Build the new XML file for all agents
    root_element = ET.Element('agents')

    for agent in agents:
        agent_element = ET.SubElement(root_element, 'agent')
        ET.SubElement(agent_element, 'id').text = agent['id']
        ET.SubElement(agent_element, 'job').text = agent['personal_id']
        
        if agent['is_rescuer']:
            ET.SubElement(agent_element, 'role').text = 'rescuer'
        else:
            ET.SubElement(agent_element, 'role').text = 'evacuee'
            
        # Add behavior traits for ALL agents
        behavior_element = ET.SubElement(agent_element, 'behavior')
        for name, _ in behavior_categories.items():
            trait_element = ET.SubElement(behavior_element, 'trait')
            ET.SubElement(trait_element, 'name').text = name
            ET.SubElement(trait_element, 'level').text = agent[name]
            
        # Add injury trait for ALL agents
        injury_element = ET.SubElement(agent_element, 'injury')
        ET.SubElement(injury_element, 'injury').text = agent['injury']
    
    # Step 12: Write the XML to a file
    tree_output = ET.ElementTree(root_element)
    ET.indent(tree_output, space="\t", level=0)
    tree_output.write(output_xml_file, encoding='utf-8', xml_declaration=True)
    
print(f"총 {number_of_files_to_create}개의 agent 파일이 '{output_directory}'에 성공적으로 생성되었습니다.")