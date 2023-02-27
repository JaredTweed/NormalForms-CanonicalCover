% This is the Main file.

% S1

im1 = imread('S1-im1.png');
im1 = im2double(imresize(im1, [750, 500])); %note-to-self, imresize stretches instead of crops

im2 = imread('S1-im2.png');
im2 = im2double(imresize(im2, [750, 500]));

im3 = imread('S1-im3.png');
im3 = im2double(imresize(im3, [750, 500]));

im4 = imread('S1-im4.png');
im4 = im2double(imresize(im4, [750, 500]));

imwrite(im1, 'S1-im1.png');
imwrite(im2, 'S1-im2.png');
imwrite(im3, 'S1-im3.png');
imwrite(im4, 'S1-im4.png');

S1 = imageDatastore({'S1-im1.png', 'S1-im2.png', 'S1-im3.png', 'S1-im4.png'});
image_manipulator('S1', S1, 4);


% S2

im1 = imread('S2-im1.png');
im1 = im2double(imresize(im1, [750, 500])); %note-to-self, imresize stretches instead of crops

im2 = imread('S2-im2.png');
im2 = im2double(imresize(im2, [750, 500]));

im3 = imread('S2-im3.png');
im3 = im2double(imresize(im3, [750, 500]));

im4 = imread('S2-im4.png');
im4 = im2double(imresize(im4, [750, 500]));

imwrite(im1, 'S2-im1.png');
imwrite(im2, 'S2-im2.png');
imwrite(im3, 'S2-im3.png');
imwrite(im4, 'S2-im4.png');

S2 = imageDatastore({'S2-im1.png', 'S2-im2.png', 'S2-im3.png', 'S2-im4.png'});
image_manipulator('S2', S2, 4);


% S3

im1 = imread('S3-im1.png');
im1 = im2double(imresize(im1, [750, 500]));

im2 = imread('S3-im2.png');
im2 = im2double(imresize(im2, [750, 500]));

im3 = imread('S3-im3.png');
im3 = im2double(imresize(im3, [750, 500]));

im4 = imread('S3-im4.png');
im4 = im2double(imresize(im4, [750, 500]));

imwrite(im1, 'S3-im1.png');
imwrite(im2, 'S3-im2.png');
imwrite(im3, 'S3-im3.png');
imwrite(im4, 'S3-im4.png');

S3 = imageDatastore({'S3-im1.png', 'S3-im2.png', 'S3-im3.png', 'S3-im4.png'});
image_manipulator('S3', S3, 4);


% S4

im1 = imread('S4-im1.png');
im1 = im2double(imresize(im1, [750, 500])); %note-to-self, imresize stretches instead of crops

im2 = imread('S4-im2.png');
im2 = im2double(imresize(im2, [750, 500]));

im3 = imread('S4-im3.png');
im3 = im2double(imresize(im3, [750, 500]));

im4 = imread('S4-im4.png');
im4 = im2double(imresize(im4, [750, 500]));

imwrite(im1, 'S4-im1.png');
imwrite(im2, 'S4-im2.png');
imwrite(im3, 'S4-im3.png');
imwrite(im4, 'S4-im4.png');

S4 = imageDatastore({'S4-im1.png', 'S4-im2.png', 'S4-im3.png', 'S4-im4.png'});
image_manipulator('S4', S4, 4);
