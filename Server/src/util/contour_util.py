import cv2
import numpy as np
import misc_math


def simplify_contour(contour, lookahead_length=8, image=None):
    """
    Simplifies the given contour, honoring corners.

    :param contour: Contour to simplify
    :param lookahead_length: Index length to look ahead on contour
    :return: Simplified contour
    """

    # Optimization variables
    contour_length = len(contour)
    half_lookahead_length = lookahead_length / 2

    # Calculate maximum deviation based on vector length
    max_deviation = lookahead_length / 2

    # Add first point to contour
    result_contour = [contour[0][0]]

    # Simplify contour
    comparison_vector = None

    i = 0
    comparison_end_point_index = lookahead_length

    while i < len(contour) - lookahead_length:

        # Extract line points
        pt1 = contour[i][0]
        pt2 = contour[(i + lookahead_length) % contour_length][0]

        # Calculate direction vector
        direction_vector = pt2 - pt1

        # Just added point - reset comparison (initial) vector
        if comparison_vector is None:

            # Calculate new comparison vector
            comparison_vector = contour[comparison_end_point_index][0] - contour[i][0]

            # Make comparison vector same length as direction vector
            comparison_vector = comparison_vector * misc_math.line_length([0.0, 0.0], direction_vector) / misc_math.line_length([0.0, 0.0], comparison_vector)

        # Check line difference from comparison vector
        if misc_math.line_length(direction_vector, comparison_vector) > max_deviation:

            # Add point to line
            result_contour.append(contour[(i + half_lookahead_length) % contour_length][0])

            # Move forward on contour
            comparison_end_point_index = i + lookahead_length
            i += half_lookahead_length

            # Reset comparison vector
            comparison_vector = None

        # Draw progress
        if image is not None:
            draw_image = draw_contour(image=image, contour=np.int32([pt1, pt2]).reshape(-1, 1, 2), name="Progress")
            draw_image = draw_points(scaled_image=draw_image, points=result_contour, scale=3, name="Progress")
            cv2.waitKey(0)

        i += 1

    # Return result contour
    return np.int32(result_contour).reshape(-1, 1, 2)


def draw_contour(image=None, scaled_image=None, contour=None, scale=3, contour_color=(255, 0, 255), points_color=None, line_width=2, name="Contour"):
    scaled_contour = contour * scale

    if image is not None:
        image_height, image_width = image.shape[:2]

        scaled_image = cv2.resize(image.copy(), (int(image_width * scale), int(image_height * scale)))
        scaled_image = cv2.cvtColor(scaled_image, cv2.COLOR_GRAY2BGR)

    cv2.drawContours(scaled_image, [scaled_contour], 0, contour_color, line_width)

    if points_color is not None:
        for p in scaled_contour:
            cv2.circle(scaled_image, (int(p[0][0]), int(p[0][1])), int(scale), points_color)

    cv2.imshow(name, scaled_image)

    return scaled_image


def draw_points(image=None, scaled_image=None, points=None, scale=3, points_color=(255, 255, 0), point_size=3, name="Contour"):
    if image is not None:
        image_height, image_width = image.shape[:2]

        scaled_image = cv2.resize(image.copy(), (int(image_width * scale), int(image_height * scale)))
        scaled_image = cv2.cvtColor(scaled_image, cv2.COLOR_GRAY2BGR)

    for p in points:
        cv2.circle(scaled_image, (int(p[0] * scale), int(p[1] * scale)), point_size, points_color)

    cv2.imshow(name, scaled_image)

    return scaled_image