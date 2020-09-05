import React from 'react';
import ScreensRoot from "./screens/Root";
import { UserProvider } from './service/UserContext';

export default function App() {
    return (
        <UserProvider>
            <ScreensRoot></ScreensRoot>
        </UserProvider>
    );
}