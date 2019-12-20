# This function calculates what is the concentration of a dissolved gas in water, knowing
# the gas concentration in headspace (ppm), the pressure of headspace (bar), the chemical
# formula of the gas, and the temperature (in celsius)
# author: alexandre.bagnoud@gmail.com
# version 14-01-2016

def dissolved_gas(gas_conc_ppm, press_bar, gas_formula, temp_celsius):
    
    import math

	# Below is a dictionary that specify for each gas, its Henry's law constant (M/atm at
	# 298.15 Kelvin) and its constant C of van't Hoff equation (in Kelvin)
	# Data from http://www.henrys-law.org/henry-3.0.pdf
	
    gas_dic = {"CO2" : (0.034, 2400), "CH4" : (0.0014, 1600), "O2": (0.0013, 1700), "H2": (0.00078, 500), "CH2F2": (0.087, 0), "C2H2" : (0.041, 1800)}
    
    if gas_formula not in gas_dic:
        
    	return "Invalid gas formula"
    	
    else:
    
    	# First the concentration in molar of the gas in headspace is calculated,
    	# based on PV = nRT (Ideal Gas Law)
    
    	gas_conc_pc = gas_conc_ppm * 1e-4
    	press_pasc = press_bar * 1e5
    	partial_press_pasc = gas_conc_pc * press_pasc / 100
        temp_kelvin = 273.15 + temp_celsius
    	gas_conc_M = partial_press_pasc / (8.314 * temp_kelvin) * 1e-3
    	
    	print "Concentration in gas phase in molar:", gas_conc_M
    	
    	# Then, we calculate the Henry's law constant in the Caq/Cgas unit, at the
    	# the specified temperature, based on equations found here:
    	# http://www.henrys-law.org/henry-3.0.pdf
    	
    	KH_M_atm_298 = gas_dic[gas_formula][0]
    	CvH = gas_dic[gas_formula][1]
    	KH_M_atm = KH_M_atm_298 * math.exp(CvH*(1/temp_kelvin-1/298.15))
    	KH_cc = KH_M_atm * temp_kelvin / 12.2
    	
    	print "KH constant (Caq/Cgas) at ", temp_kelvin, "kelvin: ", KH_cc
    	
    	# Finally, we used this new constant for calculating the dissolved gas contration
    	# in molar
    	
    	diss_conc_M = gas_conc_M * KH_cc
    	
    	print "Concentration in liquid phase in molar", diss_conc_M
    	
    	return diss_conc_M
    	
# Exemple:
    	
#print dissolved_gas(200000, 1, "O2", 20)
print dissolved_gas(400, 1, "CO2", 20)