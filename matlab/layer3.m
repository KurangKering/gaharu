[rOutput2, cOutput2] = size(output_layer2);
output_layer3 = zeros(rOutput2,cOutput2);

for i=1:rOutput2
   for j=1:cOutput2
   output_layer3(i,j) = output_layer2(i,j) / sum(output_layer2(i, :));
   end
end