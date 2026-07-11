
clear all;
close all;


vidObj = VideoReader('1.mp4');


clock = 4.9e6;



k = 1;




 while hasFrame(vidObj)

          data = readFrame(vidObj);
          data = rgb2gray(data);

%           data = 255 - data;


        data = double(data);

        data = data(end:-1:1,:);
        data = data / max(data(:));
%         [nh,nw] = size(data);
%         phasevec = 23 * randn(nh,nw);
%         phasevec = exp(1i * phasevec);
%         data = data .* phasevec;


        % data = data / max( data(:) );

        % data = data - 0.5;

        % [rows cols] = size(data);

        % data = double(data);


%         data = fftshift(data,2);
        data = ifftshift(data,2);
        data = ifft(data,[],2);


        % figure(2000);
        %
        % imagesc(abs(data));

        data = reshape(data.',1,[]);


        data = data / max( abs(data));


        iqmatrix(k,:) = data;
        k = k + 1;

end



clear data

data = reshape(iqmatrix.',1,[]);
data = data / max(abs(data));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




%  make the .dat file  float32 of IQIQIQIQIQ...
datafile = [ real(data) ; imag(data) ];

datafile = reshape(datafile, 1, []);

[filename pathname ] = uiputfile( '.bin', 'Save Bin File To:  ');

fid = fopen ([pathname filename], 'w', 'l');

fwrite(fid, datafile, 'float32');

fclose (fid);


