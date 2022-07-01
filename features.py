#!/usr/bin/env python
# coding: utf-8

# Imports
import cv2 as cv
import numpy as np
from packaging import version


# Call function SIFT
def SIFT():
    # Initiate SIFT detector
    # if opencv version is 4.4.0 or higher
    if version.parse(cv.__version__) >= version.parse('4.4.0'):
        sift = cv.SIFT_create()
    elif version.parse(cv.__version__) >= version.parse('3.2.0'):
        sift = cv.xfeatures2d.SIFT_create()

    return sift


# Call function SURF
def SURF():
    # Initiate SURF descriptor
    surf = cv.xfeatures2d.SURF_create()

    return surf


# Call function KAZE
def KAZE():
    # Initiate KAZE descriptor
    kaze = cv.KAZE_create()

    return kaze


# Call function BRIEF
def BRIEF():
    # Initiate BRIEF descriptor
    brief = cv.xfeatures2d.BriefDescriptorExtractor_create()

    return brief


# Call function ORB
def ORB():
    # Initiate ORB detector
    orb = cv.ORB_create()

    return orb


# Call function BRISK
def BRISK():
    # Initiate BRISK descriptor
    brisk = cv.BRISK_create()

    return brisk


# Call function AKAZE
def AKAZE():
    # Initiate AKAZE descriptor
    akaze = cv.AKAZE_create()

    return akaze


# Call function FREAK
def FREAK():
    # Initiate FREAK descriptor
    freak = cv.xfeatures2d.FREAK_create()

    return freak


# Call function features
def features(image):
    # Find the keypoints
    keypoints = globals.detector.detect(image, None)

    # Compute the descriptors
    keypoints, descriptors = globals.descriptor.compute(image, keypoints)

    return keypoints, descriptors


# Call function prints
def prints(keypoints,
           descriptor):
    # Print detector
    print('Detector selected:', globals.detector, '\n')

    # Print descriptor
    print('Descriptor selected:', globals.descriptor, '\n')

    # Print number of keypoints detected
    print('Number of keypoints Detected:', len(keypoints), '\n')

    # Print the descriptor size in bytes
    print('Size of Descriptor:', globals.descriptor.descriptorSize(), '\n')

    # Print the descriptor type
    print('Type of Descriptor:', globals.descriptor.descriptorType(), '\n')

    # Print the default norm type
    print('Default Norm Type:', globals.descriptor.defaultNorm(), '\n')

    # Print shape of descriptor
    print('Shape of Descriptor:', descriptor.shape, '\n')


# Call function matcher
def matcher(image1,
            image2,
            keypoints1,
            keypoints2,
            descriptors1,
            descriptors2,
            matcher,
            descriptor):
    if matcher == 'BF':
        # Se descritor for um Descritor de Recursos Locais utilizar NOME
        if (descriptor == 'SIFT') or (descriptor == 'SURF') or (descriptor == 'KAZE'):
            normType = cv.NORM_L2
        else:
            normType = cv.NORM_HAMMING

        # Create BFMatcher object
        BFMatcher = cv.BFMatcher(normType=normType,
                                 crossCheck=True)

        # Matching descriptor vectors using Brute Force Matcher
        matches = BFMatcher.match(queryDescriptors=descriptors1,
                                  trainDescriptors=descriptors2)

        # Sort them in the order of their distance
        matches = sorted(matches, key=lambda x: x.distance)

        # Draw first 30 matches
        globals.output = cv.drawMatches(img1=image1,
                                        keypoints1=keypoints1,
                                        img2=image2,
                                        keypoints2=keypoints2,
                                        matches1to2=matches[:30],
                                        outImg=None,
                                        flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        return globals.output

    elif matcher == 'FLANN':
        # FLANN parameters
        FLANN_INDEX_KDTREE = 1

        index_params = dict(algorithm=FLANN_INDEX_KDTREE,
                            trees=5)

        search_params = dict(checks=50)

        # Converto to float32
        descriptors1 = np.float32(descriptors1)
        descriptors2 = np.float32(descriptors2)

        # Create FLANN object
        FLANN = cv.FlannBasedMatcher(indexParams=index_params,
                                     searchParams=search_params)

        # Matching descriptor vectors using FLANN Matcher
        matches = FLANN.knnMatch(queryDescriptors=descriptors1,
                                 trainDescriptors=descriptors2,
                                 k=2)

        # Lowe's ratio test
        ratio_thresh = 0.7

        # "Good" matches
        good_matches = []

        # Filter matches
        for m, n in matches:
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)

        # Draw only "good" matches
        globals.output = cv.drawMatches(img1=image1,
                                        keypoints1=keypoints1,
                                        img2=image2,
                                        keypoints2=keypoints2,
                                        matches1to2=good_matches,
                                        outImg=None,
                                        flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        return globals.output
