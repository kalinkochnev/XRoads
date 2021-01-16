import React from 'react';
import ScreensRoot from "./screens/Root";
import AppState from './service/State';

export default function App() {
    return (
        <AppState>
            <ScreensRoot></ScreensRoot>
        </AppState>
    );
}