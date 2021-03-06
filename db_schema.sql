USE [muser]
GO
/****** Object:  Table [dbo].[SPOTIFY_DATA]    Script Date: 12/17/2020 12:27:50 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SPOTIFY_DATA](
	[uid] [int] IDENTITY(1,1) NOT NULL,
	[album] [varchar](500) NULL,
	[track_number] [varchar](50) NULL,
	[id] [varchar](500) NULL,
	[name] [varchar](500) NULL,
	[uri] [varchar](500) NULL,
	[acousticness] [float] NULL,
	[danceability] [float] NULL,
	[energy] [float] NULL,
	[instrumentalness] [float] NULL,
	[liveness] [float] NULL,
	[loudness] [float] NULL,
	[speechiness] [float] NULL,
	[tempo] [float] NULL,
	[valence] [float] NULL,
	[popularity] [varchar](50) NULL,
	[artist] [varchar](500) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[WKR_SPOTIFY_DATA]    Script Date: 12/17/2020 12:27:50 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[WKR_SPOTIFY_DATA](
	[uid] [int] IDENTITY(1,1) NOT NULL,
	[album] [varchar](500) NULL,
	[track_number] [varchar](500) NULL,
	[id] [varchar](500) NULL,
	[name] [varchar](500) NULL,
	[uri] [varchar](500) NULL,
	[acousticness] [varchar](500) NULL,
	[danceability] [varchar](500) NULL,
	[energy] [varchar](500) NULL,
	[instrumentalness] [varchar](500) NULL,
	[liveness] [varchar](500) NULL,
	[loudness] [varchar](500) NULL,
	[speechiness] [varchar](500) NULL,
	[tempo] [varchar](500) NULL,
	[valence] [varchar](500) NULL,
	[popularity] [varchar](500) NULL,
	[artist] [varchar](500) NULL
) ON [PRIMARY]
GO
/****** Object:  StoredProcedure [dbo].[BLD_SPOTIFY_DATA]    Script Date: 12/17/2020 12:27:50 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Ankit Raj
-- Create date: 11/14/2020
-- Description:	Creating RAW table
-- =============================================
CREATE PROC [dbo].[BLD_SPOTIFY_DATA]
	-- Add the parameters for the stored procedure here
AS
BEGIN
-- =============================================
-- INSERT into FINAL TABLE
-- =============================================
	INSERT INTO SPOTIFY_DATA (
	[album]
		  ,[track_number]
		  ,[id]
		  ,[name]
		  ,[uri]
		  ,[acousticness]
		  ,[danceability]
		  ,[energy]
		  ,[instrumentalness]
		  ,[liveness]
		  ,[loudness]
		  ,[speechiness]
		  ,[tempo]
		  ,[valence]
		  ,[popularity]
		  ,[artist]
		  )
	SELECT 
		[album]
		  ,[track_number]
		  ,[id]
		  ,[name]
		  ,[uri]
		  ,[acousticness]
		  ,[danceability]
		  ,[energy]
		  ,[instrumentalness]
		  ,[liveness]
		  ,[loudness]
		  ,[speechiness]
		  ,[tempo]
		  ,[valence]
		  ,[popularity]
		  ,[artist]
	FROM
	WKR_SPOTIFY_DATA
-- =============================================
-- TRUNCATE WORKER TABLE
-- =============================================
	TRUNCATE TABLE WKR_SPOTIFY_DATA

END
GO
