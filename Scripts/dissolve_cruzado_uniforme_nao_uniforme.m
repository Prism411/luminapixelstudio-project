function img_out	=	dissolve(imgA, imgB, tipo_dissolve, t)
    [lin1 col1] = size(imgA);
    [lin2 col2] = size(imgB);

  if tipo_dissolve == 1 %uniforme

    for i=1 : lin1
      for j=1 : col1
        img_out(i,j) =(1-t)*imgA(i,j) + t*imgB(i,j);
      endfor
    endfor

  endif

  if tipo_dissolve == 2 %nao uniforme

    for i=1 : lin1
      for j=1 : col1
        img_out(i,j) = [1-t(i,j)]*imgA(i,j) + t(i,j)*imgB(i,j)
      endfor
    endfor

  endif



  endfunction
