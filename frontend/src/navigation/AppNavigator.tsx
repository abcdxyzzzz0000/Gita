import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { useAuthStore } from '../stores/authStore';
import { RootStackParamList, TabParamList } from '../types/models';
import { theme } from '../styles/theme';

import LoginScreen from '../screens/auth/LoginScreen';
import RegisterScreen from '../screens/auth/RegisterScreen';
import HomeScreen from '../screens/HomeScreen';
import ChapterListScreen from '../screens/ChapterListScreen';
import ShlokaListScreen from '../screens/ShlokaListScreen';
import ShlokaDetailScreen from '../screens/ShlokaDetailScreen';
import SearchScreen from '../screens/SearchScreen';
import ProfileScreen from '../screens/ProfileScreen';
import BookmarksScreen from '../screens/BookmarksScreen';
import SettingsScreen from '../screens/SettingsScreen';
import LifeGuidanceScreen from '../screens/LifeGuidanceScreen';
import ReadingProgressScreen from '../screens/ReadingProgressScreen';
import WisdomHistoryScreen from '../screens/WisdomHistoryScreen';

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<TabParamList>();

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: theme.colors.primary,
        tabBarInactiveTintColor: theme.colors.outline,
        tabBarStyle: {
          backgroundColor: theme.colors.surface,
          borderTopColor: theme.colors.surfaceVariant,
        },
        headerStyle: { backgroundColor: theme.colors.surface },
        headerTintColor: theme.colors.primary,
      }}
    >
      <Tab.Screen name="Home" component={HomeScreen} options={{ title: 'Home' }} />
      <Tab.Screen name="Chapters" component={ChapterListScreen} options={{ title: 'Chapters' }} />
      <Tab.Screen name="Search" component={SearchScreen} options={{ title: 'Search' }} />
      <Tab.Screen name="Profile" component={ProfileScreen} options={{ title: 'Profile' }} />
    </Tab.Navigator>
  );
}

export default function AppNavigator() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerStyle: { backgroundColor: theme.colors.surface },
          headerTintColor: theme.colors.primary,
          headerTitleStyle: { fontWeight: '600' },
        }}
      >
        {!isAuthenticated ? (
          <>
            <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
            <Stack.Screen name="Register" component={RegisterScreen} options={{ headerShown: false }} />
            {/* Anonymous access - can browse content without auth */}
            <Stack.Screen name="MainTabs" component={MainTabs} options={{ headerShown: false }} />
            <Stack.Screen
              name="ShlokaList"
              component={ShlokaListScreen}
              options={({ route }) => ({ title: route.params.chapterTitle })}
            />
            <Stack.Screen name="ShlokaDetail" component={ShlokaDetailScreen} options={{ title: 'Verse Detail' }} />
          </>
        ) : (
          <>
            <Stack.Screen name="MainTabs" component={MainTabs} options={{ headerShown: false }} />
            <Stack.Screen
              name="ShlokaList"
              component={ShlokaListScreen}
              options={({ route }) => ({ title: route.params.chapterTitle })}
            />
            <Stack.Screen name="ShlokaDetail" component={ShlokaDetailScreen} options={{ title: 'Verse Detail' }} />
            <Stack.Screen name="Bookmarks" component={BookmarksScreen} options={{ title: 'My Bookmarks' }} />
            <Stack.Screen name="Settings" component={SettingsScreen} options={{ title: 'Settings' }} />
            <Stack.Screen name="LifeGuidance" component={LifeGuidanceScreen} options={{ title: 'Life Guidance' }} />
            <Stack.Screen name="ReadingProgress" component={ReadingProgressScreen} options={{ title: 'Reading Progress' }} />
            <Stack.Screen name="WisdomHistory" component={WisdomHistoryScreen} options={{ title: 'Wisdom History' }} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
