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
                tforms(n) = estgeotform2d(matchedRPoints, matchedRPointsPrev, 'projective', 'Confidence', 99.9999, 'MaxNumTrials', 5000,'MaxDistance',0.5);
        
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
    
    blender = vision.AlphaBlender('Operation', 'Binary mask', 'MaskSource', 'Input port');  
    
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

end
