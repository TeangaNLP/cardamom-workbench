import { useRef, forwardRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { Content, FlexboxGrid, Panel, Form, ButtonToolbar, Button, Schema } from 'rsuite';
import { Container, Navbar } from "react-bootstrap";
import axios from "axios";

import 'bootstrap/dist/css/bootstrap.css';
import "./Login.css";

const { StringType } = Schema.Types;

const model = Schema.Model({
  email: StringType()
    // .isEmail('Please enter a valid email address.')
    .isRequired('This field is required.'),
  password: StringType().isRequired('This field is required.'),
});

const TextField = forwardRef((props, ref) => {
  const { name, label, accepter, ...rest } = props;
  return (
    <Form.Group controlId={name} ref={ref}>
      <Form.ControlLabel>{label} </Form.ControlLabel>
      <Form.Control name={name} accepter={accepter} {...rest} />
    </Form.Group>
  );
});

const Login = () => {

  const formRef = useRef();
  const [formValue, setFormValue] = useState({
    email: '',
    password: '',
  });
  let navigate = useNavigate();

  const authenticateUser = () => {

    const data = new FormData()
    data.append("user", formValue.email);
    data.append("password", formValue.password);

    axios
      .post("http://127.0.0.1/api/login_user", data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then(function (response) {
        if (response.data.accept) navigate("/", { state: formValue.email });
        else console.log("User not authenticated");

      })
      .catch(function () {
        console.log("User does not exist");
      });
  }

  return (
    <div>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand >Cardamom Workbench</Navbar.Brand>
        </Container>
      </Navbar>
      <Content className="login-form">
        <FlexboxGrid justify="center">
          <FlexboxGrid.Item colspan={12}>
            <Panel header={<h3>Login</h3>} bordered>
              <Form onSubmit={authenticateUser} ref={formRef} onChange={setFormValue} formValue={formValue} model={model}>
                <TextField name="email" label="Email Address" />
                <TextField name="password" label="Password" type="password" autoComplete="off" />
                <Form.Group>
                  <ButtonToolbar>
                    <Button appearance="primary" type="submit">Submit</Button>
                  </ButtonToolbar>
                </Form.Group>
              </Form>
            </Panel>
          </FlexboxGrid.Item>
        </FlexboxGrid>
      </Content>
    </div>
  );
};
export default Login;
