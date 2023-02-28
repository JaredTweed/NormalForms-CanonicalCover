function image_manipulator(Set, Data, numImages)
    figure('Name', Set);
    % imshow([im1 im2; im3 im4]);
    % montage(Data.Files);
    imshow([readimage(Data,1) readimage(Data,2); readimage(Data,3) readimage(Data,4)]);
    
    % Part 2 & 3
    % initializing and allocating space
    fast = imageDatastore({append(Set,'-im1.png'), append(Set,'-im2.png'), append(Set,'-im3.png'), append(Set,'-im4.png')});
    fastR = imageDatastore({append(Set,'-im1.png'), append(Set,'-im2.png'), append(Set,'-im3.png'), append(Set,'-im4.png')});
    for i=1:numImages, [fast, fastR] = MakeFourRFast(Data, Set, 1, i, numImages, fast, fastR); end    
    
    % Part 4 new version
    
    I = readimage(Data,1);
    grayImage = im2gray(I);
    
    [I_fast_x, I_fast_y] = find(readimage(fast,1));
    points = [I_fast_x, I_fast_y];
    [features, points] = extractFeatures(grayImage, points, Method="SURF");
    
    [I_fastR_x, I_fastR_y] = find(readimage(fastR,1));
    pointsR = [I_fastR_x, I_fastR_y];
    [featuresR, pointsR] = extractFeatures(grayImage, pointsR, Method="SURF");
    
    % numImages = numel(Data.Files);
    tforms(numImages) = projtform2d;
    imageSize = zeros(numImages,2);
    
    imageSize(1,:) = size(grayImage);
    
    % Iterate over remaining image pairs
    for n = 2:numImages
        % Store points and features for I(n-1).
        pointsPrevious = points;
        featuresPrevious = features;
        pointsRPrevious = pointsR;
        featuresRPrevious = featuresR;
        
        for i=1:7
            i
            % Reset fast values if the first variation had bad output
            if(i ~= 1), [fast, fastR] = MakeFourRFast(Data, Set, i, n, numImages, fast, fastR); end

            % Read I(n), and initialize its features.
            I = readimage(Data, n);
            grayImage = im2gray(I);
            imageSize(n,:) = size(grayImage);
            
            [I_fast_x, I_fast_y] = find(readimage(fast,n));
            points = [I_fast_x, I_fast_y];
            [features, points] = extractFeatures(grayImage, points, Method="SURF");
            indexPairs = matchFeatures(features, featuresPrevious, 'Unique', true);
            matchedPoints = points(indexPairs(:,1), :);
            matchedPointsPrev = pointsPrevious(indexPairs(:,2), :);
        
            [I_fastR_x, I_fastR_y] = find(readimage(fastR,n));
            pointsR = [I_fastR_x, I_fastR_y];
            [featuresR, pointsR] = extractFeatures(grayImage, pointsR, Method="SURF");
            indexPairsR = matchFeatures(featuresR, featuresRPrevious, 'Unique', true);
            matchedRPoints = pointsR(indexPairsR(:,1), :);
            matchedRPointsPrev = pointsRPrevious(indexPairsR(:,2), :);
        
            % Show Matched Features
            if(n == 2)
                %figure('Name', append(Set,' fast'));
                figure(1);
                match = showMatchedFeatures(readimage(Data,n-1),readimage(Data,n),matchedPointsPrev,matchedPoints,'montage');
                saveas(match, append(Set,'-fastMatch.png'));
        
                %figure('Name', append(Set,' fastR'));
                figure(1);
                match = showMatchedFeatures(readimage(Data,n-1),readimage(Data,n),matchedRPointsPrev,matchedRPoints,'montage');
                saveas(match, append(Set,'-fastRMatch.png'));
            end

            if(n == 3)
                %figure('Name', append(Set,' fast'));
                figure(3);
                showMatchedFeatures(readimage(Data,n-1),readimage(Data,n),matchedPointsPrev,matchedPoints,'montage');
                
                %figure('Name', append(Set,' fastR'));
                figure(3);
                showMatchedFeatures(readimage(Data,n-1),readimage(Data,n),matchedRPointsPrev,matchedRPoints,'montage');
            end
    
            try
                % Estimate the transformation between I(n) and I(n-1).
                tforms(n) = estgeotform2d(matchedRPoints, matchedRPointsPrev,...
                    'projective', 'Confidence', 99.9999, 'MaxNumTrials', 5000,'MaxDistance',0.5);
        
                % Allows code to continue if estgeotform returns an invertible matrix
                if(rank(tforms(n).T) == size(tforms(n).T,2))
                    break
                end
            catch
                continue
            end

            if(rank(tforms(n).T) ~= size(tforms(n).T,2))
                continue
            end

            break
        
        end

        tforms(n).A = tforms(n-1).A * tforms(n).A; 
    end
    
    
    % Part 5 (and 6)
    figure(2);
    
    %tform.T is the homography
    
    for i = 1:numImages%numel(tforms)           
        [xlim(i,:), ylim(i,:)] = outputLimits(tforms(i), [1 imageSize(i,2)], [1 imageSize(i,1)]);
    end
    
    maxImageSize = max(imageSize);
    
    % Find the minimum and maximum output limits. 
    xMin = min([1; xlim(:)]);
    xMax = max([maxImageSize(2); xlim(:)]);
    
    yMin = min([1; ylim(:)]);
    yMax = max([maxImageSize(1); ylim(:)]);
    
    % Width and height of panorama.
    width  = round(xMax - xMin);
    height = round(yMax - yMin);
    
    % Initialize the "empty" panorama.
    panorama = zeros([height width 3], 'like', I);
    
    blender = vision.AlphaBlender('Operation', 'Binary mask', ...
        'MaskSource', 'Input port');  
    
    % Create a 2-D spatial reference object defining the size of the panorama.
    xLimits = [xMin xMax];
    yLimits = [yMin yMax];
    panoramaView = imref2d([height width], xLimits, yLimits);
    
    % Create the panorama.
    for i = 1:numImages
        
        I = readimage(Data, i);   
       
        % Transform I into the panorama.
        warpedImage = imwarp(I, tforms(i), 'OutputView', panoramaView);
                      
        % Generate a binary mask.    
        mask = imwarp(true(size(I,1),size(I,2)), tforms(i), 'OutputView', panoramaView);
        
        % Overlay the warpedImage onto the panorama.
        panorama = step(blender, panorama, warpedImage, mask);
    end

    imwrite(panorama, append(Set,'-panorama.png'));
    
    figure(6);
    imshow(panorama)



    
    % Part 4 old version (worked with only 2 images)
    
    %{
    % figure(4)
    
    [fast_im1x, fast_im1y] = find(fast_im1);
    [fast_im2x, fast_im2y] = find(fast_im2);
    
    fast_im1_find = [fast_im1x, fast_im1y];
    
    [im1_features, im1_VP] = extractFeatures(im2gray(im1), [fast_im1x fast_im1y], Method="SURF");
    [im2_features, im2_VP] = extractFeatures(im2gray(im2), [fast_im2x fast_im2y], Method="SURF");
    
    indexPairs = matchFeatures(im1_features,im2_features, 'Unique', true);
    
    im1_matchedPoints = im1_VP(indexPairs(:, 1), :);
    im2_matchedPoints = im2_VP(indexPairs(:, 2), :);
    
    % showMatchedFeatures(im1,im2,im1_matchedPoints,im2_matchedPoints,'montage');
    %}







    % Part 5 old attempts (kept because they might be useful later)

    %{
    
    % tform = fitgeotrans(im1_points, im2_points, 'projective');
    
    % estgeoform uses MSAC which is a variation of RANSAC % Note to self:
    % function will error if not allowed enough trials or MaxDistance.
    % This function will sometimes fail and sometimes work.
    tform = estgeotform2d(im1_matchedPoints, im2_matchedPoints,'projective', 'Confidence', 90, 'MaxNumTrials', 1000000,'MaxDistance',20);
    tform.T % This is the homography
    
    % for i = 1:numel(tforms)           
    %     [xlim(:), ylim(:)] = outputLimits(tform, [1 size(im2gray(im1))], [1 size(im2gray(im2))]);    
    % end
    
    % estimateFundamentalMatrix();
    % homography = estimateFundamentalMatrix(im1_matchedPoints, im2_matchedPoints,Method="RANSAC", NumTrials=1000,DistanceThreshold=0.01,Confidence=99,InlierPercentage=60);
    % homograph()
    
    % homography = estgeotform2d(im1_matchedPoints, ...
    %     im2_matchedPoints,"projective", 'Confidence', 99.9, 'MaxNumTrials', 2000);
    
    % im1_prime=homography*im1;
    
    % displacementField = homography2displacementField(tform.T, size(im2));
    
    % im2_warped = imwarp(im2, projective2d(homography),"OutputView", imref2d([height width], xLimits, yLimits));
    % im2_warped = imwarp(im2, projective2d(homography).T, "nearest");
    im2_warped = imwarp(im2, tform, "nearest");
    % im2_warped1 = imwarp(im2, projective2d(homography).T, "nearest");
    
    imshow(im2_warped);
    
    % panorama = stitch(im1, im2_warped);
    
    %estimateGeometricTransform2d
    
    % panorama = imageStitching(im1, im2, homography, 'OutputView', outputView);
    
    % stitched_im = imwarp(im2, homography.T, 'OutputView', imref2d(size(im1)));
    % imshow(stitched_im);
    % imshow(im1_prime);
    
    
    % RANSAC = vision.GeometricTransformEstimator('Transform','Projective','InlierOutputPort',true,'AlgebraicDistanceThreshold',3,'RefineTransformMatrix',true,'NumRandomSamplings',2000);
    % transformer = vision.GeometricTransformer;
    % [tform, inliers] = step(RANSAC, im1_matchedPoints.Location, im2_matchedPoints.Location);
    
% function displacementField = homography2displacementField(H, imageSize)
%     [X, Y] = meshgrid(1:imageSize(2), 1:imageSize(1));
%     XY = [X(:) Y(:) ones(numel(X), 1)];
%     XY_transformed = (H * XY')';
%     X_transformed = reshape(XY_transformed(:, 1) ./ XY_transformed(:, 3), imageSize(1), imageSize(2));
%     Y_transformed = reshape(XY_transformed(:, 2) ./ XY_transformed(:, 3), imageSize(1), imageSize(2));
%     displacementField(:, :, 1) = X - X_transformed;
%     displacementField(:, :, 2) = Y - Y_transformed;
% end

    %}
end