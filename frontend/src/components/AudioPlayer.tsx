import React, { useState, useRef } from 'react';
import { View, StyleSheet, Platform } from 'react-native';
import { IconButton, Text, ProgressBar } from 'react-native-paper';
import { theme, spacing } from '../styles/theme';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api';

interface AudioPlayerProps {
  shlokaId: string;
  available: boolean;
}

export default function AudioPlayer({ shlokaId, available }: AudioPlayerProps) {
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  if (!available) {
    return (
      <View style={styles.container}>
        <Text variant="bodySmall" style={styles.unavailable}>
          Audio not yet available for this verse
        </Text>
      </View>
    );
  }

  const cleanup = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  const togglePlayback = () => {
    setError(false);

    if (playing && audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      cleanup();
      setPlaying(false);
      setProgress(0);
      return;
    }

    // Use HTML5 Audio on web
    if (Platform.OS === 'web') {
      const audioUrl = `${API_BASE_URL}/shlokas/${shlokaId}/audio`;
      const audio = new Audio(audioUrl);
      audioRef.current = audio;

      audio.onplay = () => {
        setPlaying(true);
        intervalRef.current = setInterval(() => {
          if (audio.duration > 0) {
            setProgress(audio.currentTime / audio.duration);
          }
        }, 200);
      };

      audio.onended = () => {
        cleanup();
        setPlaying(false);
        setProgress(0);
      };

      audio.onerror = () => {
        cleanup();
        setPlaying(false);
        setProgress(0);
        setError(true);
      };

      audio.play().catch(() => {
        setError(true);
      });
    } else {
      // Native: show placeholder message
      setError(true);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.controls}>
        <IconButton
          icon={playing ? 'pause-circle' : 'play-circle'}
          iconColor={theme.colors.primary}
          size={40}
          onPress={togglePlayback}
        />
        <View style={styles.progressSection}>
          <ProgressBar
            progress={progress}
            color={theme.colors.primary}
            style={styles.progressBar}
          />
          <Text variant="labelSmall" style={styles.label}>
            {playing ? 'Playing...' : 'Tap to play chanting'}
          </Text>
        </View>
      </View>
      {error && (
        <Text variant="bodySmall" style={styles.error}>
          Unable to play audio
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: spacing.sm,
  },
  controls: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  progressSection: {
    flex: 1,
    marginRight: spacing.md,
  },
  progressBar: {
    height: 4,
    borderRadius: 2,
  },
  label: {
    color: theme.colors.outline,
    marginTop: 4,
  },
  unavailable: {
    color: theme.colors.outline,
    fontStyle: 'italic',
    textAlign: 'center',
    paddingVertical: spacing.sm,
  },
  error: {
    color: theme.colors.error,
    textAlign: 'center',
  },
});
