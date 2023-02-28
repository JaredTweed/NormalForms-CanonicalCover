function [fast, fastR] = MakeFourRFast(Data, Set, constantCombo, imageNumber, SetSize, fast, fastR)
    figure(1);

    fast_im = zeros(size(readimage(fast, imageNumber),1), size(readimage(fast, imageNumber),2), SetSize);
    fastR_im = zeros(size(readimage(fastR, imageNumber),1), size(readimage(fastR, imageNumber),2), SetSize);

    % Part 2
    
    % detect
    fast_im(:,:,imageNumber) = my_fast_detector(readimage(Data,imageNumber),constantCombo);
    
    % save
    if(imageNumber == 1), imwrite(fast_im(:,:,imageNumber), append(Set,'-fast.png'));
    else, imwrite(fast_im(:,:,imageNumber), append(Set,'-fast-im', num2str(imageNumber),'.png')); end
    
    % store
    if(imageNumber == 1), fast.Files{imageNumber} = append(Set,'-fast.png');
    else, fast.Files{imageNumber} = append(Set,'-fast-im', num2str(imageNumber),'.png'); end    

    % Part 3
    fastR_im(:,:,imageNumber) = my_fastR_detector(readimage(Data,imageNumber), fast_im(:,:,imageNumber));
    
    if(imageNumber == 1), imwrite(fastR_im(:,:,imageNumber), append(Set,'-fastR.png'));
    else, imwrite(fastR_im(:,:,imageNumber), append(Set,'-fastR-im', num2str(imageNumber),'.png')); end
    
    if(imageNumber == 1), fastR.Files{imageNumber} = append(Set,'-fastR.png');
    else, fastR.Files{imageNumber} = append(Set,'-fastR-im', num2str(imageNumber),'.png'); end    

end