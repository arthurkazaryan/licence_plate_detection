
def get_vehicle_registration_plate(coordinates):
    veh_reg_plate = dict()
    for i, reg_plate in enumerate(coordinates['vehicle_registration_plate']):
        veh_coordinates = [coor_i for coor_i in coordinates['car']
                            if coor_i[0] < reg_plate[0] and
                                coor_i[1] < reg_plate[1] and
                                coor_i[2] > reg_plate[2] and
                                coor_i[3] > reg_plate[3]]
        veh_reg_plate['vehicle_'+str(i)] = {'vehicle': veh_coordinates[0], 'vehicle_registration_plate': reg_plate}

    return veh_reg_plate