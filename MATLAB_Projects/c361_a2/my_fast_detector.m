function [fast_points] = my_fast_detector(image, constantSet)

    im = im2double(im2gray(image));
    %im = imadjust(im,stretchlim(im),[]); % I produced many images without
    %this, but it helps the algorithm's consistency for testing
    if(constantSet == 1)
        N = 6;   % best variation: 6
        t = 0.2; % best variation: 0.2
    elseif(constantSet == 2)
        N = 5;
        t = 0.2;
    elseif(constantSet == 3)
        N = 5;
        t = 0.3;
    elseif(constantSet == 4)
        N = 4;
        t = 0.4;
    elseif(constantSet == 5)
        N = 4;
        t = 0.3;
    elseif(constantSet == 6)
        N = 4;
        t = 0.2;
    else
        N = 4;
        t = 0.1;
    end

    tic

    p = zeros(750,500,16);
    p_diff = zeros(750,500,16);
    fast_points = zeros(750,500);

    p(4:(end-3),4:(end-3),1) = im(4-3:(end-3)-3, 4:(end-3));
    p(4:(end-3),4:(end-3),2) = im(4-3:(end-3)-3, 4+1:(end-3)+1);
    p(4:(end-3),4:(end-3),3) = im(4-2:(end-3)-2, 4+2:(end-3)+2);
    p(4:(end-3),4:(end-3),4) = im(4-1:(end-3)-1, 4+3:(end-3)+3);
    p(4:(end-3),4:(end-3),5) = im(4:(end-3), 4+3:(end-3)+3);
    p(4:(end-3),4:(end-3),6) = im(4+1:(end-3)+1, 4+3:(end-3)+3);
    p(4:(end-3),4:(end-3),7) = im(4+2:(end-3)+2, 4+2:(end-3)+2);
    p(4:(end-3),4:(end-3),8) = im(4+3:(end-3)+3, 4+1:(end-3)+1);
    p(4:(end-3),4:(end-3),9) = im(4+3:(end-3)+3, 4:(end-3));
    p(4:(end-3),4:(end-3),10) = im(4+3:(end-3)+3, 4-1:(end-3)-1);
    p(4:(end-3),4:(end-3),11) = im(4+2:(end-3)+2, 4-2:(end-3)-2);
    p(4:(end-3),4:(end-3),12) = im(4+1:(end-3)+1, 4-3:(end-3)-3);
    p(4:(end-3),4:(end-3),13) = im(4:(end-3), 4-3:(end-3)-3);
    p(4:(end-3),4:(end-3),14) = im(4-1:(end-3)-1, 4-3:(end-3)-3);
    p(4:(end-3),4:(end-3),15) = im(4-2:(end-3)-2, 4-2:(end-3)-2);
    p(4:(end-3),4:(end-3),16) = im(4-3:(end-3)-3, 4-1:(end-3)-1);

    for i=1:16
        p_diff(4:(end-3),4:(end-3), i) = p(4:(end-3),4:(end-3),i) - im(4:(end-3),4:(end-3));        
    end

    for i=1:16
        if(i<=16-N+1)
            window = p_diff(:,:,i:i+N-1);
        else
            window = p_diff(:,:,[1:(N-1)-(16-i), i:16]);
        end
        fast_points = fast_points | sum(window > t, 3) == N | sum(window < -t, 3) == N;
    end

    fast_time = toc
end