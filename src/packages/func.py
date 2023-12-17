import asyncio

import discord
from discord.ext import commands

class func_inter:
    async def disable_dm(interaction: discord.Interaction):
        """
        ダイレクトメッセージ内で特定の操作を無効にする(スラッシュコマンド)
        """
        if not interaction.guild:
            await interaction.response.send_message(embed=discord.Embed(title="このコマンドはダイレクトメッセージでは無効に設定されています。"), ephemeral=True)
            return True
        else:
            return False

class func_ctx:
    async def disable_dm(ctx: commands.Context):
        """
        ダイレクトメッセージ内で特定の操作を無効にする(メッセージコマンド)
        """
        if not ctx.guild:
            msg = await ctx.reply(embed=discord.Embed(title="このコマンドはダイレクトメッセージでは無効に設定されています。"))
            await asyncio.sleep(2.5)
            await msg.delete()
            return True
        else:
            return False

PERMISSIONS = {
    "add_reactions": "リアクションの追加",
    "administrator": "管理者",
    "attach_files": "ファイルを添付",
    "ban_members": "メンバーをBAN",
    "change_nickname": "ニックネームの変更",
    "connect": "ボイスチャンネルに接続",
    "create_instant_invite": "招待を作成",
    "create_private_threads": "プライベートスレッドの作成",
    "create_public_threads": "公開スレッドの作成",
    "deafen_members": "メンバーのスピーカーをミュート",
    "embed_links": "埋め込みリンク",
    "external_emojis": "外部の絵文字の使用",
    "external_stickers": "外部のスタンプを使用",
    "kick_members": "メンバーをキック",
    "manage_channels": "チャンネルの管理",
    "manage_emojis": "絵文字の管理",
    "manage_events": "イベントの管理",
    "manage_guild": "サーバーの管理",
    "manage_messages": "メッセージの管理",
    "manage_nicknames": "ニックネームの管理",
    "manage_roles": "ロールの管理",
    "manage_threads": "スレッドの管理",
    "manage_webhooks": "ウェブフックの管理",
    "mention_everyone": "@everyone、@here、全てのロールにメンション",
    "moderate_members": "メンバーのタイムアウト",
    "move_members": "メンバーのボイスチャンネルを移動",
    "mute_members": "メンバーをミュート",
    "priorite_spealer": "優先スピーカー",
    "read_message_history": "メッセージ履歴を読む",
    "read_messages": "メッセージを読む",
    "request_to_speak": "スピーカー参加をリクエスト",
    "send_messages_in_threads": "スレッドでメッセージを送信",
    "send_messages": "メッセージを送信",
    "send_tts_messages": "TTSメッセージを送信",
    "speak": "ボイスチャンネルで発言",
    "stream": "配信",
    "use_application_commands": "スラッシュコマンドの使用",
    "use_embedded_activities": "埋め込みアプリケーションの起動",
    "use_voice_activation": "音声検出の使用",
    "view_audit_log": "監査ログを表示",
    "view_guild_insights": "サーバーインサイトの閲覧"
}