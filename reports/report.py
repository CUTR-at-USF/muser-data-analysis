'''
/*
 * Copyright (C) 2019-2020 University of South Florida
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 '''

import pandas as pd
import plotly.express as px
import datetime

class MuserReport:
    def __init__(self, data, writer):
        self.df = pd.read_csv(data)
        self.writer = writer
        self.generate_report()


    def _extract_date(self, time_stamp, is_milli=False):
        if is_milli:
            seconds = time_stamp / 1e3
        else:
            seconds = time_stamp
        dt = datetime.datetime.fromtimestamp(seconds)
        return dt.strftime('%Y-%m-%d')


    def _extract_time(self, time_stamp, is_milli=False):
        if is_milli:
            seconds = time_stamp / 1e3
        else:
            seconds = time_stamp
        dt = datetime.datetime.fromtimestamp(seconds)
        return dt.strftime('%H:%M:%S')

    def clean_df(self):
        df_copy = self.df.copy()
        df_copy["event_type"] = df_copy["player_event_type"].fillna(df_copy["ui_event_type"])
        df_copy = df_copy[df_copy["event_type"].notnull()]
        df_copy = df_copy[df_copy["song_date_added"].notnull()]
        df_copy["download_date"] = df_copy["song_date_added"].apply(self._extract_date)
        df_copy["activity_time"] = df_copy["event_current_time_in_milliseconds"].apply(
            lambda x: self._extract_time(x, is_milli=True))
        return df_copy

    def download_dates(self, df):
        download_date_data = pd.DataFrame(df["download_date"].value_counts()).reset_index()
        download_date_data.columns = ["download_date", "count"]
        download_date_data.sort_values("download_date", inplace=True, ignore_index=True)
        fig = px.line(download_date_data, x="download_date", y="count", title="Songs downloaded over time")
        fig.write_image("download_date_data.png")
        return download_date_data


    def user_activity(self, df):
        user_activity_dist = pd.DataFrame(df["user_id"].value_counts()).reset_index()
        user_activity_dist.columns = ["user_id", "activity_count"]
        low_threshold = user_activity_dist["activity_count"].quantile(q=0.4)
        high_threshold = user_activity_dist["activity_count"].quantile(q=0.9)
        user_activity_dist["activity_level"] = [
            "low" if x < low_threshold else "high" if x > high_threshold else "medium" for x in
            user_activity_dist["activity_count"]]
        fig = px.pie(names=user_activity_dist["activity_level"].value_counts().index,
                     values=user_activity_dist["activity_level"].value_counts().values, width=800,
                     title="User activity distribution")
        fig.write_image("user_activity.png")
        return user_activity_dist


    def unique_songs_stats(self, df):
        grouped_event_data = df.groupby("event_type")
        target_keys = ["PAUSE", "SKIP"]
        unique_songs_play = set(grouped_event_data.get_group("PLAY")["song_id"].tolist())
        unique_songs_pause = set(grouped_event_data.get_group("PAUSE")["song_id"].tolist())
        unique_songs_skip = set(grouped_event_data.get_group("SKIP")["song_id"].tolist())
        list_completed_songs = []
        for song in unique_songs_play:
            if song not in unique_songs_pause and song not in unique_songs_skip:
                print("Song id: {} is unique, adding to the list".format(song))
                list_completed_songs.append(song)
        unique_songs_stats = pd.DataFrame(columns=["count"],
                                          index=["Unique songs PLAYED", "Unique songs PAUSED", "Unique songs SKIPPED",
                                                 "Unique songs PLAYED without PAUSE or SKIP"])
        unique_songs_stats.loc["Unique songs PLAYED", "count"] = len(unique_songs_play)
        unique_songs_stats.loc["Unique songs PAUSED", "count"] = len(unique_songs_pause)
        unique_songs_stats.loc["Unique songs SKIPPED", "count"] = len(unique_songs_skip)
        unique_songs_stats.loc["Unique songs PLAYED without PAUSE or SKIP", "count"] = len(list_completed_songs)
        fig = px.pie(names=unique_songs_stats.index, values=unique_songs_stats["count"].values,
                     title="% completed play(without pausing or skipping)", width=800)
        fig.write_image("unique_songs_stats.png")
        return unique_songs_stats


    def days_active(self, df):
        user_days_active = df[["user_id", "activity_count"]]
        user_days_active["days_active(%)"] = user_days_active["activity_count"].apply(
            lambda x: x / user_days_active["activity_count"].sum())
        fig = px.bar(user_days_active, x="user_id", y="days_active(%)", title="% days active", height=800)
        fig.write_image("user_activity_dist.png")
        return user_days_active


    def activity_time(self, df):
        activity_time_data = pd.DataFrame(df["activity_time"].value_counts()).reset_index()
        activity_time_data.columns = ["activity_time", "count"]
        fig = px.histogram(df, x="activity_time", color="user_id",
                           title="Activity by Time of day among active users")
        fig.write_image("activity_time_data.png")
        return activity_time_data


    def generate_report(self):
        muser_data = self.clean_df()
        muser_data.to_excel(self.writer, sheet_name="cleaned_muser_data", index=False)

        download_date_data = self.download_dates(muser_data)
        download_date_data.to_excel(self.writer, sheet_name="download_date_data", index=False)
        # workbook = self.writer.book
        worksheet = self.writer.sheets["download_date_data"]
        worksheet.insert_image("F1", "download_date_data.png")

        user_activity_dist = self.user_activity(muser_data)
        user_activity_dist.to_excel(self.writer, sheet_name="user_activity_dist", index=False)
        # workbook = self.writer.book
        worksheet = self.writer.sheets["user_activity_dist"]
        worksheet.insert_image("F1", "user_activity_dist.png")

        unique_songs_stats = self.unique_songs_stats(muser_data)
        unique_songs_stats.to_excel(self.writer, sheet_name="unique_songs_stats", index=True)
        # workbook = self.writer.book
        worksheet = self.writer.sheets["unique_songs_stats"]
        worksheet.insert_image("F1", "unique_songs_stats.png")

        user_days_active = self.days_active(user_activity_dist)
        user_days_active.to_excel(self.writer, sheet_name="user_days_active", index=False)
        # workbook = self.writer.book
        worksheet = self.writer.sheets["user_days_active"]
        worksheet.insert_image("F1", "user_days_active.png")

        activity_time_data = self.activity_time(muser_data)
        activity_time_data.to_excel(self.writer, sheet_name="activity_time_data", index=False)
        # workbook = self.writer.book
        worksheet = self.writer.sheets["activity_time_data"]
        worksheet.insert_image("F1", "activity_time_data.png")
        print("Worksheets added to the excel workbook")
