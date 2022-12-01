# Final work on the course "Python developer" on the project "Employment Assistance"

## Assignment to the final work:

It is possible that we want to show our friends photos from social networks, but social networks may not be available for some reason. Let's protect ourselves from this.
You need to write a program to backup photos from the profile (avatars) of the VK user to the Yandex.Disk cloud storage.
For the names of photos, use the number of likes, if the number of likes is the same, then add the upload date.

Save information on saved photos to a json file.

## Task:

You need to write a program that will:

- Get photos from your profile. To do this, use the [photos.get](https://dev.vk.com/method/photos.get) method.
- Save photos of the maximum size (width/height in pixels) on Yandex.Disk.
- To name photos, use the number of likes.
- Save information on photos to a json file with the results.
  
Please note: the token for VK can be obtained by following the [instructions](https://docs.google.com/document/d/1_xt16CMeaEir-tWLbUFyleZl6woEdJt-7eyva1coT3w/edit).

## Input data:

The user enters:

- VK user id;
- a token from the [Yandex.Disk Polygon](https://yandex.ru/dev/disk/poligon/). Important: You don't need to publish the token to github!

## Output data:

1. json file with information on the file:
``` 
    [{
    "file_name": "34.jpg",
    "size": "z"
    }]
 ```   
2. The modified Ya.Disk where the photos were added.

## Mandatory requirements for the program:

1. Use the REST API of the Ya.Disk and the key obtained from the polygon.
2. You need to create a separate folder for the uploaded photos.
3. Save the specified number of photos (5 by default) of the largest size (width/height in pixels) on the Yandex.Disk.
4. Make a progress bar or logging to track the program process.
5. The program code must satisfy PEP8.
6. The program should have its own separate repository.
7. All dependencies must be specified in the file requiremеnts.txt .​