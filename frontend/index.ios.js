import React, { Component } from 'react';
import { WebView } from 'react-native';

import {
  AppRegistry,
  StyleSheet,
  Text,
  View
} from 'react-native';

class frontend extends Component {
  render() {
    return (
      <WebView
        source={{uri: 'http://localhost:3000/'}}
        style={{marginTop: 20}}
      />
    );
  }
}

AppRegistry.registerComponent('frontend', () => frontend);
