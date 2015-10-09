import networkx as nx


class UserVariables(object):
    # these will be assigned as the user determines which values they would like 
    # then the global var's above will be assigned the according to these values
    self.LATMIN = '5.0' #min latitude; -ve values in the SH e.g. 5S = -5                                                  
    self.LATMAX = '19.0' #max latitude; -ve values in the SH e.g. 5S = -5 20.0                                            
    self.LONMIN = '-5.0' #min longitude; -ve values in the WH e.g. 59.8W = -59.8 -30                                       
    self.LONMAX = '9.0' #min longitude; -ve values in the WH e.g. 59.8W = -59.8  30                                     
    self.XRES = 4.0              #x direction spatial resolution in km                                                    
    self.YRES = 4.0              #y direction spatial resolution in km                                                      
    self.TRES = 1                #temporal resolution in hrs                                                              
    self.LAT_DISTANCE = 111.0    #the avg distance in km for 1deg lat for the region being considered                     
    self.LON_DISTANCE = 111.0    #the avg distance in km for 1deg lon for the region being considered                     
    self.STRUCTURING_ELEMENT = [[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]
                           ] #the matrix for determining the pattern for the contiguous boxes and must                
                        #have same rank of the matrix it is being compared against                                
                        #criteria for determining cloud elements and edges                                  
    self.T_BB_MAX = 243  #warmest temp to allow (-30C to -55C according to Morel and Sensi 2002)                          
    self.T_BB_MIN = 218  #cooler temp for the center of the system                                     
    self.CONVECTIVE_FRACTION = 0.90 #the min temp/max temp that would be expected in a CE.. this is highly   
                           #conservative (only a 10K difference)                                         
    self.MIN_MCS_DURATION = 3    #minimum time for a MCS to exist
    self.AREA_MIN = 2400.0       #minimum area for CE criteria in km^2 according to Vila et al. (2008) is 2400                 
    self.MIN_OVERLAP = 10000.00   #km^2  from Williams and Houze 1987, indir ref in Arnaud et al 1992                            
    #---the MCC criteria
    self.ECCENTRICITY_THRESHOLD_MAX = 1.0  #tending to 1 is a circle e.g. hurricane,
    self.ECCENTRICITY_THRESHOLD_MIN = 0.70 #tending to 0 is a linear e.g. squall line
    self.OUTER_CLOUD_SHIELD_AREA = 80000.0 #km^2
    self.INNER_CLOUD_SHIELD_AREA = 30000.0 #km^2
    self.OUTER_CLOUD_SHIELD_TEMPERATURE = 233 #in K
    self.INNER_CLOUD_SHIELD_TEMPERATURE = 213 #in K                                                                 
    self.MINIMUM_DURATION = 6  #min number of frames the MCC must exist for (assuming hrly frames, MCCs is 6hrs) 
    self.MAXIMUM_DURATION = 24 #max number of framce the MCC can last for   
    
class GraphVariables(object):
    self.edgeWeight = [1, 2, 3] # weights for the graph edges
    self.CLOUD_ELEMENT_GRAPH = nx.DiGraph() # graph obj for the CEs meeting criteria
    self.PRUNED_GRAPH = nx.DiGraph() # graph meeting the CC criteria
    
def define_user_variables():
    # this is where users will determine the variables the want
    userVars = UserVariables()

    # users can reassign the variables based on prompts given to them
    
    # return the new userVars
    return userVars

def define_graph_variables():
    graphVars = GraphVariables()
    return graphVars

