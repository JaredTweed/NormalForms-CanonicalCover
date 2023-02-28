function [fastR_image] = my_fastR_detector(image, fastImage)

    k = 0.04; % best variation: 0.04

    im = im2double(im2gray(image));

    tic

    % Gradient calculation
    sobel = [-1 0 1;-2 0 2;-1 0 1];
    gaus = fspecial('gaussian', 5, 1);
    dog = conv2(gaus, sobel);
    Ix = imfilter(im, dog);
    Iy = imfilter(im, dog');

    % Gaussian
    Ix2g = imfilter(Ix.^2, gaus);
    Iy2g = imfilter(Iy.^2, gaus);
    Ixyg = imfilter(Ix .* Iy, gaus);

    % Cornerness
    % M = [Ix2g Ixyg; Ixyg Iy2g];
    M_determinant = (Ix2g .* Iy2g) - (Ixyg .* Ixyg);
    M_trace = Ix2g + Iy2g;
    cornernessImage = M_determinant - k*(M_trace).^2;

    % Points after threshold is applied
    thresh = 0.00001;
    fastR_image = fastImage & cornernessImage > thresh;

    fastR_time = toc
end