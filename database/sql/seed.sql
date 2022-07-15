\c workbench;

INSERT INTO users (name, email, password) VALUES ('test', 'test@test.com', 'test123');

INSERT INTO languages (language_name, iso_code, requested) VALUES ('English', 'en', FALSE);

INSERT INTO languages (language_name, iso_code, requested) VALUES ('Old Irish', 'sga', FALSE);

INSERT INTO uploaded_files (name, content, user_id, language_id) VALUES ('a.txt', 'Lorem ipsum dolor sit amet, consectetur adipiscing  elit. Donec eu urna iaculis, consequat ex et, suscipit arcu. Duis laoreet consectetur viverra. Mauris odio mauris, tempus nec libero nec, commodo hendrerit eros. Nullam porta et elit eget fermentum. Fusce vehicula ac eros bibendum consectetur. Sed maximus, risus id vestibulum imperdiet, ligula mi accumsan tellus, eget blandit eros magna tincidunt dolor. Praesent lobortis non quam ac sodales. Donec a ligula eu leo consequat porta sit amet id mauris. Integer bibendum purus id orci posuere volutpat. In efficitur elit vitae mauris volutpat, non pellentesque quam consequat. Cras dui risus, condimentum a tortor quis, volutpat pellentesque diam. Vivamus feugiat posuere erat ut sollicitudin. Quisque sed ex ac turpis tincidunt porttitor id at lectus. Pellentesque feugiat magna ut elit bibendum faucibus.', 1, 1);

INSERT INTO uploaded_files (name, content, user_id, language_id) VALUES ('a.txt', '.i. biuusa ocirbáig darfarcennsi frimaccidóndu\n\n.i. niarformut fribsi asbiursa inso arropad maith limsa labrad ilbelre dúibsi\n\n.i. isipersin crist dagníusa sin\n\n.i. ó domanicc foirbthetu ní denim gnímu macthi act rísam nem bimmi æcni et bimmi foirbthi uili\n\n.i. isocprecept soscéli attó\n\n.i. ished inso noguidimm .i. conducaid etargne ṅ dǽ et conaroib temel innatol domunde tarrosc fornanme\n\n.i. hore nondobmolorsa et nom móidim indib\n\n.i. amal nondafrecṅdirccsa\n\n.i. is inse ṅduit nitú nodnai(l) acht ishé not ail\n\n.i. madarlóg pridchasa .i. armetiuth et mothoschith nímbia fochricc dar hési moprecepte\n\n.i. coníarimse peccad libsi uili ɫ. aratartsa fortacht dúibsi arnap trom fuirib fornóinur\n\n.i. cote mothorbese dúib madamne labrar\n\n.i. nihed notbeir ínem ciabaloingthech\n\nAcht nammáa issamlid istorbe són co etercerta anasbera et conrucca inætarcne cáich\n\n.i. léic uáit innabiada mílsi ettomil innahí siu dommeil do chenél arnáphé som conéit détso\n\n	.i. isamlid dorígeni dia corp duini ó ilballaib\n\n	.i. act basamlid dúib cid immeícndarcus', 1, 2)

INSERT INTO annotations (token, reserved_token, start_index, end_index, token_language_id, type, uploaded_file_id) VALUES ('Lorem', TRUE, 0, 4, 1, 'manual', 1);

INSERT INTO annotations (token, reserved_token, start_index, end_index, token_language_id, type, uploaded_file_id) VALUES ('ipsum', TRUE, 6, 11, 1, 'manual', 1);

