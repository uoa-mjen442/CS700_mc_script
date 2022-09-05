function [voltage] = test_script(inputv)
assignin('base', 'input_voltage', double(inputv))
data = sim('basic_model');
%plot(data.voltage);
%there isnt a default method for retrieving timeseries data in a tabular
%format nightmare nightmare nightmare dont look at this code its better for
%your eyes
voltage = zeros(51, 2);
k = 0;
for i = 1:51
    voltage(i, 2) = getdatasamples(data.voltage, [i]);
    voltage(i, 1) = k;
    k = k + 0.2;
end
end