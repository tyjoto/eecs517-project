import os
from pprint import pprint

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

import eecs517project.utls.constants as c
import eecs517project.utls.helpers as h
from eecs517project.particles import Particle

style.use("bmh")
path = os.path.dirname(__file__)

seed = 10 
rng = np.random.default_rng(seed)


def iterator(val, dictionary:dict):
    total = np.zeros_like(val)
    for key in dictionary.keys():
        total += dictionary[key](val)
    return total

def make_total_mean_free_path_func(background:dict, cross_section:dict ):
    lambda_funcs = []
    for gas in background.keys():
        gas_p = gas+"+"
        if gas_p in cross_section.keys():
            def cross_section_iterator(val):
                return iterator(val, cross_section[gas_p])

        def calc_total_mean_free_path_for_a_background_gas(x, E):
            Ng = background[gas](x)
            sigma = cross_section_iterator(E)
            temp = np.multiply(Ng,sigma)
            with np.errstate(divide='ignore'):
                temp = np.where(temp !=0, np.divide(1,temp), np.inf)

            return temp
        lambda_funcs.append(calc_total_mean_free_path_for_a_background_gas)
    def calc_total_mean_free_path_for_all_background_gases(x,E):
        lambdaT = np.zeros_like(E)
        for func in lambda_funcs:
            lambdaT += func(x,E)
        #print(lambdaT)
        return lambdaT
    return calc_total_mean_free_path_for_all_background_gases

        


def loop_of_particles(particles: dict, background: dict , cross_sections: dict, domain:dict, **kwargs):
    for parts in particles.keys():
        particles[parts] = loop_of_particles_for_one(particles[parts], background, cross_sections, domain)

    return particles

def loop_of_particles_for_one(particles, background: dict, cross_sections:dict, domain: dict):
    distance = determine_where_collision_occurs_for_particles(particles, background, cross_sections)
    indices, particles = determine_if_particles_make_it_to_beam_dump_and_update_particle_position(
        domain, distance, particles
    )
    if len(indices[0]) != 0:
        particles = determine_type_of_collision_and_update_particle_velocity(
            indices, particles, background, cross_sections, domain, distance
        )
    return particles
def determine_where_collision_occurs_for_particles(particles, background: dict, cross_sections:dict):
    vel = particles.vel[:,2]
    vel = vel.reshape((vel.shape[0],1))
    ergT = particles.erg[:,2].reshape(vel.shape)
    p_size = ergT.size

    lambdaT = make_total_mean_free_path_func(background, cross_sections)
    
    R = rng.random((p_size,1))
    lambdaT_values = lambdaT(particles.pos, particles.ergT)
    #print("LambdaT\n",lambdaT_values)
    sign = np.where(vel>=0,1, -1)#.reshape(R.shape)
    rD = np.multiply(np.multiply(np.log(R),lambdaT_values), sign)
    D = np.subtract(
        particles.pos,
        rD
        
    )
    #print("D",D)
    return D
def determine_if_particles_make_it_to_beam_dump_and_update_particle_position(domain, distance, particles):
    vel = particles.vel[:,2].reshape((particles.vel.shape[0],1))
    indecies_for_did_not_make_contact = np.where((distance < domain["Z"]) & (distance>0.0) & (vel>0.0))
    # for particles that make it
    new_pos = np.where(distance>=domain["Z"], domain["Z"], np.where(distance<0,0.0,distance))
    particles.pos = new_pos


    return indecies_for_did_not_make_contact, particles

def indicies_of_indices(ncolls, indices, these_indices):
    array_indices = np.array(indices)
    #print("array_inidices")
    #pprint(array_indices)
    #print(array_indices.shape)

    # get indices
    x = array_indices[0].reshape((ncolls,1))
    #print(x)
    x = x[these_indices]
    #print(x)
    y = np.zeros_like(x)
    this_collision_indices = (x,y)
    return this_collision_indices

def determine_type_of_collision_and_update_particle_velocity(indices, particles, background, cross_sections, domain, distance):
    #print("determine_type_of_collision...")
    #pprint(indices)
    ncolls = len(indices[0])
    #print(ncolls)
    ngas = len(background)

    # first dertermine which gas species (background)
    if ngas == 1:
        gas = list(background.keys())[0]
    else:
        raise NotImplementedError

    # determine which collision type
    gas_p = gas +"+"
    # get energies of particles that had collisons to determine total cross section
    ergT0 = particles.erg[:,2]
    ergT0 = ergT0.reshape((ergT0.shape[0],1))
    ergT = ergT0[indices].reshape((ncolls,1))
    # calculate total cross section
    sigmaT0 = iterator(ergT0, cross_sections[gas_p])
    sigmaT = sigmaT0[indices].reshape((ncolls,1))
    #print(indices)
    #pprint(sigmaT0)
    #pprint(sigmaT)
    # pick rando
    R = rng.random((ncolls,1))
    # initialize sigma
    sigma = np.zeros_like(ergT)

    for key, func in cross_sections[gas_p].items():
        #print(key)
        # get sigma for first collision type to make ratio
        sigma += func(ergT)
        ratio = sigma/sigmaT
        #pprint(sigma)
        #pprint(ratio)
        #pprint(R)
        # determine if this is right collison
        right_collision_indices = np.where(R<=ratio)
        wrong_collision_indices = np.where(R>ratio)
        #print("RCI")
        #pprint(right_collision_indices)
        #print("WCI")
        #pprint(wrong_collision_indices)

        # now determine new velocites based on collision type
        #array of indices
        this_collision_indices = indicies_of_indices(ncolls, indices, right_collision_indices)
        #print("this_collision_indices")
        #pprint(this_collision_indices)


        # now update with new velocities
        len_this_collision_indices = len(this_collision_indices[0])
        if len_this_collision_indices == 0:
            pass
        else:
            if key == "CEX":
                vth = 0.0 # change later
                vel = np.array([vth, vth, vth])
                # just x because vel is 3D
                particles.vel[this_collision_indices[0]] = vel            
            elif key == "MEX":
                #print(ncolls)
                vel = particles.vel[this_collision_indices[0]]
                #pos = np.zeros((vel.shape[0],1))
                pos = particles.pos[this_collision_indices[0]]
                #print("Prepos", pos)
                #lambda_ = np.divide(1, np.multiply(cross_sections[gas_p]["MEX"](vel), background["Xe"](pos)))
                #post = np.array(np.log(R[right_collision_indices])*lambda_[:,2]).reshape((pos.shape)) # next position
                #print("post",post)
                #pos = np.subtract(pos, post)
                vel = h.isotropic_scattering(vel)
                #print(vel)
                #print("pos", pos)
                m_i, W = particles.m_i,particles.W
                #print(m_i,W)
                temp_particles = Particle(m_i,pos=pos, vel=vel, amu=False, W = W)
                temp_particles = loop_of_particles({gas_p:temp_particles},background, cross_sections, domain)
                #temp_particles = {gas_p: temp_particles}
                particles.vel[this_collision_indices[0]] = temp_particles[gas_p].vel
                particles.pos[this_collision_indices[0]] = temp_particles[gas_p].pos
                #print(particles.vel)
                #print(particles.pos)
            else:
                raise NotImplementedError
            
            

        # update how many colls still need to be resolved
        ncolls -= len_this_collision_indices

        # check if any more colls to resolve
        if ncolls == 0:
            break
        # reset for next cross section
        #not_this_collision_indices = tuple(array_indices[wrong_collision_indices])
        not_this_collision_indices = indicies_of_indices(ncolls+len_this_collision_indices,indices,wrong_collision_indices)
        #print("not_this_collision_indices")
        #pprint(not_this_collision_indices)
        if not not_this_collision_indices:
            print("ERROR")
            not_this_collision_indices = tuple([np.array([]), np.array([])])
        # get energies of particles that had collisons to determine total cross section
        ergT = ergT0[not_this_collision_indices].reshape((ncolls,1))
        #print(R)
        # calculate total cross section
        sigmaT = sigmaT0[not_this_collision_indices].reshape((ncolls,1))
        # slice rando
        R = R[wrong_collision_indices].reshape((ncolls,1))
        #print(Rtemp)
        # get sigma for first collision type to make ratio
        sigma = sigma[wrong_collision_indices].reshape((ncolls,1))
        ratio = sigma/sigmaT
        # remap indices

        #indices = tuple(np.array(indices)[wrong_collision_indices])
        indices = indicies_of_indices(ncolls+len_this_collision_indices,indices,wrong_collision_indices)
        #print(indices)
    return particles


