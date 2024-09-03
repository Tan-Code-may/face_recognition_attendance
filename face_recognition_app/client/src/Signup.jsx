import React, { useState } from 'react';
import './styles.css';
import { Link } from 'react-router-dom';

const signupInputs = [
    {
        label: "First Name",
        type: "text",
        show: false,
        validated: "",
        id: "c"
    }, {
        label: "Last Name",
        type: "text",
        show: false,
        validated: "",
        id: "c"
    }, {
        label: "Username",
        type: "email",
        show: false,
        validated: "",
        id: "d"
    }, {
        label: "Password",
        type: "password",
        show: false,
        validated: "",
        id: "e"
    }, {
        label: "Re-Enter Password",
        type: "password",
        show: false,
        validated: "",
        id: "f"
    }
];

const SignupWrapper = () => {
    const [signUp, setSignUp] = useState(true);
    const [signupInputsState, setSignupInputsState] = useState(signupInputs);
    const [userType, setUserType] = useState("student");
    const [images, setImages] = useState([null, null, null, null, null]);

    const inUpClick = () => {
        setSignUp(!signUp);
        animateFields("signupInputs");
    };

    const animateFields = (formName) => {
        let newForm = signupInputsState.slice();
        let stagger = (i) => {
            if (i < newForm.length) {
                setTimeout(() => {
                    newForm[i].show = !newForm[i].show;
                    setSignupInputsState(newForm);
                    stagger(i + 1);
                }, 70);
            }
        };
        stagger(0);
    };

    const submitForm = (e) => {
        e.preventDefault();
        const requiredImages = userType === "student" ? 5 : 1;
        if (images.slice(0, requiredImages).every(img => img !== null)) {
            console.log("User Type:", userType);
            console.log("Selected Images:", images.slice(0, requiredImages));
        } else {
            alert(`Please upload all ${requiredImages} image(s).`);
        }
    };

    const validateField = (event, id) => {
        let newState = signupInputsState.slice();
        const fieldInState = newState.find(field => field.id === id);
        fieldInState.validated = event.target.value.length > 0 ? true : false;
        setSignupInputsState(newState);
    };

    const handleImageChange = (index, file) => {
        let newImages = images.slice();
        newImages[index] = file;
        setImages(newImages);
    };

    return (
        <div>
            <SignUp
                signUp={signUp}
                inputs={signupInputsState}
                inUpClick={inUpClick}
                submitForm={submitForm}
                validateField={validateField}
                userType={userType}
                setUserType={setUserType}
                handleImageChange={handleImageChange}
            />
        </div>
    );
};

const SignUp = ({ inputs, signUp, inUpClick, submitForm, validateField, userType, setUserType, handleImageChange }) => (
    <div className={signUp ? "sign-up" : "sign-up sign-up-closed"}>
        <h1>Sign Up</h1>
        <hr />
        <Form
            inputs={inputs}
            submitForm={submitForm}
            validateField={validateField}
            userType={userType}
            setUserType={setUserType}
            handleImageChange={handleImageChange}
        />
        <LoginLink inUpClick={inUpClick} />
    </div>
);

const Form = ({ inputs, submitForm, validateField, userType, setUserType, handleImageChange }) => (
    <form onSubmit={submitForm}>
        {inputs.map((input) => (
            <Input
                key={input.id}
                label={input.label}
                type={input.type}
                show={input.show}
                validated={input.validated}
                id={input.id}
                validateField={validateField}
            />
        ))}
        <div className="radio-group">
            <label className="radio-label">
                <input
                    className="radio-input"
                    type="radio"
                    name="userType"
                    value="student"
                    checked={userType === "student"}
                    onChange={() => setUserType("student")}
                />
                Student
            </label>
            <label className="radio-label">
                <input
                    className="radio-input"
                    type="radio"
                    name="userType"
                    value="professor"
                    checked={userType === "professor"}
                    onChange={() => setUserType("professor")}
                />
                Professor
            </label>
        </div>

        {/* Conditionally render image upload fields based on userType */}
        {userType === "student"
            ? Array.from({ length: 5 }).map((_, index) => (
                <div className="field" key={index}>
                    <label className="label">Upload Image {index + 1}</label>
                    <br />
                    <input
                        className="input"
                        type="file"
                        accept="image/*"
                        onChange={(e) => handleImageChange(index, e.target.files[0])}
                    />
                </div>
            ))
            : (
                <div className="field">
                    <label className="label">Upload Image</label>
                    <br />
                    <input
                        className="input"
                        type="file"
                        accept="image/*"
                        onChange={(e) => handleImageChange(0, e.target.files[0])}
                    />
                </div>
            )}
        <Submit />
    </form>
);

const Submit = () => (
    <div>
        <hr />
        <button className="submit-button" type="submit">Submit</button>
    </div>
);

const Input = ({ label, type, show, validated, id, validateField }) => (
    <div className={show ? "field field-in" : "field"}>
        <label className="label">{label}
            <i className={validated ? "fa fa-check animate-check" : ""} aria-hidden="true"></i>
        </label>
        <br />
        <input
            className="input"
            type={type}
            onBlur={(event) => validateField(event, id)}
        />
    </div>
);

const LoginLink = ({ inUpClick }) => (
    <div className="signup-link">
        <p className="in-out">
            Already have an account? {" "}
            <Link to="/login">Log in Here</Link>
        </p>
    </div>
);

export default SignupWrapper;