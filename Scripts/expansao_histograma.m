function [img_out] = expansao_histograma(img)

	[lin col] = size(img)
	img_out = zeros(lin col);
	img = im2double(img);

	rmin = min(img(:));
	rmax = max(img(:));
	L = 256;

	for i = 1:lin
	  for j = 1:col
		    img_out(i, j) = round ( ((img(i,j)-rmin))*(L-1) );
	    endfor
  endfor

	img_out = uint8(img_out);
endfunction
