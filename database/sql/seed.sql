\c workbench;

INSERT INTO users (name, email, password) VALUES ('test', 'test@test.com', 'test123');

INSERT INTO uploaded_files (name, content, user_id) VALUES ('a.txt', 'Lorem ipsum dolor sit amet, consectetur adipiscing  elit. Donec eu urna iaculis, consequat ex et, suscipit arcu. Duis laoreet consectetur viverra. Mauris odio mauris, tempus nec libero nec, commodo hendrerit eros. Nullam porta et elit eget fermentum. Fusce vehicula ac eros bibendum consectetur. Sed maximus, risus id vestibulum imperdiet, ligula mi accumsan tellus, eget blandit eros magna tincidunt dolor. Praesent lobortis non quam ac sodales. Donec a ligula eu leo consequat porta sit amet id mauris. Integer bibendum purus id orci posuere volutpat. In efficitur elit vitae mauris volutpat, non pellentesque quam consequat. Cras dui risus, condimentum a tortor quis, volutpat pellentesque diam. Vivamus feugiat posuere erat ut sollicitudin. Quisque sed ex ac turpis tincidunt porttitor id at lectus. Pellentesque feugiat magna ut elit bibendum faucibus.', 1);

INSERT INTO annotations (token, reserved_token, start_index, end_index, text_language, token_language, type, uploaded_file_id) VALUES ('Lorem', TRUE, 0, 4, 'IDK', 'IDK', 'automatic', 1);

INSERT INTO annotations (token, reserved_token, start_index, end_index, text_language, token_language, type, uploaded_file_id) VALUES ('ipsum', TRUE, 6, 11, 'IDK', 'IDK', 'manual', 1);