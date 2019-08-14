from object_constructors import *

missionXML ='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Appeltjes!</Summary>
              </About>
              
              <ServerSection>
                <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,2*3,2;1"/>
                  <DrawingDecorator>

						<!-- Walls around the experimental ground -->
						<DrawCuboid x1="-50" x2="50" z1="-50" z2="-50" y1="4" y2="100" type="obsidian"/>
						<DrawCuboid x1="-50" x2="50" z1="50" z2="50" y1="4" y2="100" type="obsidian"/>
						<DrawCuboid x1="-50" x2="-50" z1="50" z2="-50" y1="4" y2="100" type="obsidian"/>
						<DrawCuboid x1="50"  x2="50" z1="-50" z2="50" y1="4" y2="100" type="obsidian"/>
						
						<!-- Add trees / food -->
            ''' + gen_lots_of_food() + '''
							
					</DrawingDecorator> 
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                        <Name>Adam</Name>
                  
                      <AgentStart>
        
                        <Placement x="0" y="4" z="0" yaw="0"/>
                       
                        <Inventory>
                          <InventoryItem slot="0" type="diamond_sword"/>
                          <InventoryItem slot="1" type="apple"/>
                        </Inventory>
                        
                      </AgentStart>
            
                <AgentHandlers>
                  <MissionQuitCommands/>
                  <ObservationFromFullStats/>
            <!--    <ObservationFromFullInventory/>  -->
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''




















