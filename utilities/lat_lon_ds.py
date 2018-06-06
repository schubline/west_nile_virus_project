def lat_lon_ds(p_1, p_2):
    """Argument 'p1' is a list of decimal [lat, lon] coords in degrees. 'p2' is another list.
    Function returns the distance between them in meters, without correction for curvature of the earth.
    Distance will be slightly underestimated by a fraction approximately (t - sin(t)), where t is the angular separation
    between the two points in radians.  For 1 degree of latitude, the relative error is < 1e-6."""
    
    import numpy as np
    
    # http://frederic.chambat.free.fr/geophy/inertie_pepi01/article.pdf
    # Equitorial radius, eqn. 15
    R_earth = 6378137  # meters
    
    # Distance btw O'Hare and Wrigley field is 20879.8 meters, along a great circle
    # coords are [41.94885800000001, 87.65774809999999], [41.9741625, 87.9073214]
    # According to http://edwilliams.org/gccalc.htm
    # This gives a Chicago-area correction factor of (20879.8/20849.9), 
    # where the denominator is calculated using uncorrected R_earth.
    
    R = R_earth*(20879.8/20849.9)
    
    theta_1 = (90 - p_1[0])*(2*np.pi/360)
    phi_1 = p_1[1]*(2*np.pi/360)
    theta_2 = (90 - p_2[0])*(2*np.pi/360)
    phi_2 = p_2[1]*(2*np.pi/360)
    
    def x(r,phi,theta):
        return r*np.sin(theta)*np.cos(phi)
    
    def y(r,phi,theta):
        return r*np.sin(theta)*np.sin(phi)
    
    def z(r,phi,theta):
        return r*np.cos(theta)
    
    # Calculate euclidean distance
    delta_s= np.sqrt(
        (x(R, phi_1, theta_1) - x(R, phi_2, theta_2))**2 + \
        (y(R, phi_1, theta_1) - y(R, phi_2, theta_2))**2 + \
        (z(R, phi_1, theta_1) - z(R, phi_2, theta_2))**2 \
    )

    return delta_s