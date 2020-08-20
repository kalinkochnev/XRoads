This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Temporary REST API calls to django backend

While we are figuring out the login process and where/how we will store the auth token, here is a temporary procedure for dealing with it: 

* Use any rest client to register a valid user
```
curl -X POST http://localhost:8000/auth/registration/ -d '{"email":"akochnev+xruser2@gmail.com", "password1":"nimda123", "password2":"nimda123"}' -H "Content-Type:application/json"
```

* Verify the user from the URL that is printed on the django console
The message on the console looks something like this: 
```
To confirm this is correct, go to http://localhost:8000/auth/registration/account-confirm-email/Mg:1k8cFU:T73WqnRYwgQWscswsF_w4Jeq5jQ/
```
* Use a rest client to login with the new user and get a valid token
```bash
curl -X POST http://localhost:8000/auth/login/ -d '{"email":"akochnev+xruser2@gmail.com", "password":"nimda123"}' -H "Content-Type:application/json"
{"key":"5b4ab7859fc63d623df1d8a5072f519aca9c8abb"}
```

* Put the token in the .env.development file as the value of the REACT_APP_XROADS_TEMP_TOKEN env var
## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: https://facebook.github.io/create-react-app/docs/code-splitting

### Analyzing the Bundle Size

This section has moved here: https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size

### Making a Progressive Web App

This section has moved here: https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app

### Advanced Configuration

This section has moved here: https://facebook.github.io/create-react-app/docs/advanced-configuration

### Deployment

This section has moved here: https://facebook.github.io/create-react-app/docs/deployment

### `npm run build` fails to minify

This section has moved here: https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify
