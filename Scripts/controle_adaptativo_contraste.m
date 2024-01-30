function [img_out] = controle_adaptativo_contraste (img, c)
  [lin col] = size(img);
  img_out = zeros(lin col);


  for i = 2:(lin-1)
    for i = 2 :(lin-1)
      viz = [img(i-1,j), img(i, j-1), img(i, j+1), img(i+1, j)];
      media = mean(viz);
      des = std(viz);
          if des != 0;
              img_out(i, j) = media + (c/desvio) * (img(i,j) - media)
          endif
        else
              img_out(i,j) = img(i,j);
    endfor
  endfor

  img_out = uint8(img_out);

  endfunction
