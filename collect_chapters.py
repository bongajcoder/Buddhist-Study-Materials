#!/usr/bin/env python3
"""
Script to collect Buddhist study chapters from sokaglobal.org
"""
import requests
from bs4 import BeautifulSoup
import os
import time
from pathlib import Path

BASE_URL = "https://www.sokaglobal.org"

# Book 1: The Wisdom for Creating Happiness and Peace
BOOK1_CHAPTERS = [
    # Chapter 1
    ("chapter-1-1.html", "Chapter 1.1 - Leading the Happiest of Lives"),
    ("chapter-1-2.html", "Chapter 1.2 - Absolute Happiness and Relative Happiness"),
    ("chapter-1-3.html", "Chapter 1.3 - Happiness Is Forged amid Life's Challenges"),
    ("chapter-1-4.html", "Chapter 1.4 - Happiness Lies within Us"),
    ("chapter-1-5.html", "Chapter 1.5 - Creating a Life of Genuine Freedom"),
    ("chapter-1-6.html", "Chapter 1.6 - The Six Conditions for Happiness"),
    ("chapter-1-7.html", "Chapter 1.7 - Confronting Life's Fundamental Sufferings Head-On"),
    # Chapter 2
    ("chapter-2-1.html", "Chapter 2.1 - Living with Optimism"),
    ("chapter-2-2.html", "Chapter 2.2 - The Key to Happiness Is Inner Transformation"),
    ("chapter-2-3.html", "Chapter 2.3 - The Life State of Practitioners of the Mystic Law"),
    ("chapter-2-4.html", "Chapter 2.4 - Our Happiness Is Determined by Our Inner Life Condition"),
    ("chapter-2-5.html", "Chapter 2.5 - Happiness Is Found Where We Are"),
    ("chapter-2-6.html", "Chapter 2.6 - Activating the Limitless Life Force of Buddhahood"),
    ("chapter-2-7.html", "Chapter 2.7 - Establishing the World of Buddhahood as Our Basic Life Tendency"),
    ("chapter-2-8.html", "Chapter 2.8 - You Are All Noble Buddhas"),
    # Chapter 3
    ("chapter-3-1.html", "Chapter 3.1 - The Gohonzon—the Fundamental Object of Devotion"),
    ("chapter-3-2.html", "Chapter 3.2 - Never Seek This Gohonzon outside Yourself"),
    ("chapter-3-3.html", "Chapter 3.3 - The Gohonzon Is Found in Faith Alone"),
    ("chapter-3-4.html", "Chapter 3.4 - The Real Aspect and Power of the Gohonzon"),
    ("chapter-3-5.html", "Chapter 3.5 - The Gohonzon Is the Mirror That Reflects Our Lives"),
    ("chapter-3-6.html", "Chapter 3.6 - The Profound Meaning of Nam-myoho-renge-kyo"),
    ("chapter-3-7.html", "Chapter 3.7 - Embracing the Gohonzon Is in Itself Attaining Enlightenment"),
    ("chapter-3-8.html", "Chapter 3.8 - The Mystic Law Exists within Our Lives"),
    ("chapter-3-9.html", "Chapter 3.9 - A Practice Accessible to All"),
    ("chapter-3-10.html", "Chapter 3.10 - Chanting Nam-myoho-renge-kyo Is the Key to Victory in Life"),
    ("chapter-3-11.html", "Chapter 3.11 - The Lotus Sutra Is a Scripture of Cosmic Humanism"),
    ("chapter-3-12.html", "Chapter 3.12 - Gongyo Encompasses the Heart of the Lotus Sutra"),
    ("chapter-3-13.html", "Chapter 3.13 - Gongyo—A Ceremony in Which Our Lives Commune with the Universe"),
    ("chapter-3-14.html", "Chapter 3.14 - Polishing Our Lives through Chanting Nam-myoho-renge-kyo"),
    ("chapter-3-15.html", "Chapter 3.15 - Change Starts from Prayer"),
    ("chapter-3-16.html", "Chapter 3.16 - Chanting Nam-myoho-renge-kyo Freely"),
    ("chapter-3-17.html", "Chapter 3.17 - Chanting with Unwavering Conviction"),
    ("chapter-3-18.html", "Chapter 3.18 - Developing a Strong Inner Core"),
    ("chapter-3-19.html", "Chapter 3.19 - Faith Is a Lifelong Pursuit"),
    ("chapter-3-20.html", "Chapter 3.20 - The Universal Language of Buddhas and Bodhisattvas"),
    # Chapter 4
    ("chapter-4-1.html", "Chapter 4.1 - Living with an Awareness of the Importance of the Heart"),
    ("chapter-4-2.html", "Chapter 4.2 - Appreciation and Joy Multiply Our Good Fortune"),
    ("chapter-4-3.html", "Chapter 4.3 - Those Who Smile Are Strong"),
    ("chapter-4-4.html", "Chapter 4.4 - Polishing Our Hearts to Shine like Diamonds"),
    ("chapter-4-5.html", "Chapter 4.5 - Mastering Our Minds"),
    ("chapter-4-6.html", "Chapter 4.6 - Remaining True to One's Commitment in Faith"),
    ("chapter-4-7.html", "Chapter 4.7 - When Our Life State Changes, the World around Us Changes"),
    ("chapter-4-8.html", "Chapter 4.8 - Devoting Ourselves to Our Mission"),
    ("chapter-4-9.html", "Chapter 4.9 - Nothing Is Ever Wasted in Buddhism"),
    ("chapter-4-10.html", "Chapter 4.10 - Cultivating a Lofty Life State Imbued with the Four Virtues"),
    # Chapter 5
    ("chapter-5-1.html", "Chapter 5.1 - We Are the Protagonists of Our Own Lives"),
    ("chapter-5-2.html", "Chapter 5.2 - Earthly Desires Lead to Enlightenment"),
    ("chapter-5-3.html", "Chapter 5.3 - Changing Poison into Medicine"),
    ("chapter-5-4.html", "Chapter 5.4 - Creating the Future with the Buddhism of True Cause"),
    ("chapter-5-5.html", "Chapter 5.5 - Living with Joy throughout All"),
    ("chapter-5-6.html", "Chapter 5.6 - Both Suffering and Joy Are a Part of Life"),
    ("chapter-5-7.html", "Chapter 5.7 - Difficulties Are a Driving Force for Growth"),
    ("chapter-5-8.html", "Chapter 5.8 - Polishing Ourselves through Adversity"),
    ("chapter-5-9.html", "Chapter 5.9 - Winter Always Turns to Spring"),
    ("chapter-5-10.html", "Chapter 5.10 - The Principle of Lessening Karmic Retribution"),
    # Chapter 6
    ("chapter-6-1.html", "Chapter 6.1 - Still I Will Bloom"),
    ("chapter-6-2.html", "Chapter 6.2 - Bringing Out Our Positive Qualities"),
    ("chapter-6-3.html", "Chapter 6.3 - Live True to Yourself"),
    ("chapter-6-4.html", "Chapter 6.4 - Appreciating Your Uniqueness"),
    ("chapter-6-5.html", "Chapter 6.5 - Developing Your Own Individuality"),
    ("chapter-6-6.html", "Chapter 6.6 - Be a Shining Presence like the Sun"),
    ("chapter-6-7.html", "Chapter 6.7 - Advancing Freely and Steadily"),
    ("chapter-6-8.html", "Chapter 6.8 - Everyone Has a Noble Mission"),
    ("chapter-6-9.html", "Chapter 6.9 - Building a Harmonious World of Brilliant Diversity"),
    ("chapter-6-10.html", "Chapter 6.10 - The Wisdom for Fostering the Positive Potential in All People"),
    # Chapter 7
    ("chapter-7-1.html", "Chapter 7.1 - Joy Means That Oneself and Others Together Experience Joy"),
    ("chapter-7-2.html", "Chapter 7.2 - The Bodhisattva Way Enables Us to Benefit Both Ourselves and Others"),
    ("chapter-7-3.html", "Chapter 7.3 - The Path of Mutual Respect and Growth"),
    ("chapter-7-4.html", "Chapter 7.4 - Treasuring the People Right in Front of Us"),
    ("chapter-7-5.html", "Chapter 7.5 - We Are Enriched by Helping Others"),
    ("chapter-7-6.html", "Chapter 7.6 - The Bodhisattva Practice of Respecting All People"),
    ("chapter-7-7.html", "Chapter 7.7 - Accumulating Treasures of the Heart"),
    ("chapter-7-8.html", "Chapter 7.8 - The Supreme Path of Benefiting Others"),
    # Chapter 8
    ("chapter-8-1.html", "Chapter 8.1 - Struggling with Illness Can Forge Invincible Spiritual Strength"),
    ("chapter-8-2.html", "Chapter 8.2 - Transforming the Sufferings of Birth, Aging, Sickness, and Death"),
    ("chapter-8-3.html", "Chapter 8.3 - Chanting Nam-myoho-renge-kyo Is the Wellspring of Life Force"),
    ("chapter-8-4.html", "Chapter 8.4 - Turning Illness into an Impetus for Growth"),
    ("chapter-8-5.html", "Chapter 8.5 - Falling Ill Is Not a Sign of Defeat"),
    ("chapter-8-6.html", "Chapter 8.6 - The Buddhist View of Illness"),
    ("chapter-8-7.html", "Chapter 8.7 - Faith Means to Continue to Believe until the Very End"),
    ("chapter-8-8.html", "Chapter 8.8 - Laugh Off the Devil of Illness"),
    ("chapter-8-9.html", "Chapter 8.9 - Four Mottoes for Good Health"),
    # Chapter 9
    ("chapter-9-1.html", "Chapter 9.1 - Enjoying a Rewarding and Fulfilling Third Stage of Life"),
    ("chapter-9-2.html", "Chapter 9.2 - Striving to the End with a Spirit of Ceaseless Challenge"),
    ("chapter-9-3.html", "Chapter 9.3 - The Secret to a Vigorous Old Age"),
    ("chapter-9-4.html", "Chapter 9.4 - A Source of Hope and Inspiration for a Happy Aging Society"),
    ("chapter-9-5.html", "Chapter 9.5 - Building an Eternal Palace in Our Lives"),
    ("chapter-9-6.html", "Chapter 9.6 - There Is No Retirement from Faith"),
    ("chapter-9-7.html", "Chapter 9.7 - Changing Our Attitude toward Aging"),
    ("chapter-9-8.html", "Chapter 9.8 - Making an Art of Life"),
    # Chapter 10
    ("chapter-10-1.html", "Chapter 10.1 - Consolidating the State of Buddhahood in This Lifetime"),
    ("chapter-10-2.html", "Chapter 10.2 - Death Gives Greater Meaning to Life"),
    ("chapter-10-3.html", "Chapter 10.3 - The Buddhist View of Life That Transcends the Suffering of Death"),
    ("chapter-10-4.html", "Chapter 10.4 - The Oneness of Life and Death"),
    ("chapter-10-5.html", "Chapter 10.5 - Savoring Joy in Both Life and Death"),
    ("chapter-10-6.html", "Chapter 10.6 - Advancing on the Path of Buddhahood in Both Life and Death"),
    ("chapter-10-7.html", "Chapter 10.7 - The Death of Someone Close to Us"),
    ("chapter-10-8.html", "Chapter 10.8 - Our Own Attainment of Buddhahood Enables the Deceased to Attain Buddhahood"),
    ("chapter-10-9.html", "Chapter 10.9 - Ties Based on the Mystic Law Are Eternal"),
    ("chapter-10-10.html", "Chapter 10.10 - Sudden and Untimely Deaths"),
    ("chapter-10-11.html", "Chapter 10.11 - Clear Proof of Attaining Buddhahood"),
    ("chapter-10-12.html", "Chapter 10.12 - Transforming the Sufferings of Birth and Death"),
    # Chapter 11
    ("chapter-11-1.html", "Chapter 11.1 - The Theme of The Human Revolution and The New Human Revolution"),
    ("chapter-11-2.html", "Chapter 11.2 - Establishing the Life State of Buddhahood"),
    ("chapter-11-3.html", "Chapter 11.3 - Human Revolution—A Concept of Key Importance for the 21st Century"),
    ("chapter-11-4.html", "Chapter 11.4 - Indicators of Human Revolution"),
    ("chapter-11-5.html", "Chapter 11.5 - The True Benefit of Faith Is Human Revolution"),
    ("chapter-11-6.html", "Chapter 11.6 - A Never-ending Effort to Transform Reality"),
    ("chapter-11-7.html", "Chapter 11.7 - Developing Inner Strength"),
    ("chapter-11-8.html", "Chapter 11.8 - A Process of Unending Inner Transformation and Self-Improvement"),
    # Chapter 12
    ("chapter-12-1.html", "Chapter 12.1 - The Principle of Voluntarily Assuming the Appropriate Karma"),
    ("chapter-12-2.html", "Chapter 12.2 - Fulfilling Our Vow as Bodhisattvas of the Earth"),
    ("chapter-12-3.html", "Chapter 12.3 - The Great Drama of Human Revolution"),
    ("chapter-12-4.html", "Chapter 12.4 - All Karma Has Profound Meaning"),
    ("chapter-12-5.html", "Chapter 12.5 - Chanting Nam-myoho-renge-kyo Holds the Key to Changing Poison into Medicine"),
    ("chapter-12-6.html", "Chapter 12.6 - Our Personal Experiences of Changing Karma Give Hope to Others"),
    ("chapter-12-7.html", "Chapter 12.7 - A Triumphant Drama"),
    ("chapter-12-8.html", "Chapter 12.8 - Those Who Suffer the Most Can Attain Buddhahood without Fail"),
    ("chapter-12-9.html", "Chapter 12.9 - A New Guide for Humanity"),
    # Chapter 13
    ("chapter-13-1.html", "Chapter 13.1 - Our Own Human Revolution Is the Key to Achieving Family Harmony"),
    ("chapter-13-2.html", "Chapter 13.2 - The Miraculous Words Thank You"),
    ("chapter-13-3.html", "Chapter 13.3 - Showing Appreciation for Our Parents Is the Heart of Buddhism"),
    ("chapter-13-4.html", "Chapter 13.4 - Advice on Raising and Educating Children in the Home"),
    ("chapter-13-5.html", "Chapter 13.5 - Accepting Others for Who They Are"),
    ("chapter-13-6.html", "Chapter 13.6 - A Partnership of Deepening Love and Respect"),
    # Chapter 14
    ("chapter-14-1.html", "Chapter 14.1 - Buddhism Teaches How to Live as a Human Being"),
    ("chapter-14-2.html", "Chapter 14.2 - Be People Who Shine through Their Behavior"),
    ("chapter-14-3.html", "Chapter 14.3 - Being Responsible, Good Citizens"),
    ("chapter-14-4.html", "Chapter 14.4 - Kosen-rufu Starts from Actions in Daily Life"),
    ("chapter-14-5.html", "Chapter 14.5 - Buddhism Manifests Itself in Society"),
    ("chapter-14-6.html", "Chapter 14.6 - Leading a Contributive Life"),
    ("chapter-14-7.html", "Chapter 14.7 - The Greater Self of the Bodhisattva Way"),
    ("chapter-14-8.html", "Chapter 14.8 - The Qualities of Global Citizens"),
    ("chapter-14-9.html", "Chapter 14.9 - Leading Noble Lives as Global Citizens"),
    # Chapter 15
    ("chapter-15-1.html", "Chapter 15.1 - Adversity as a Source of Pride"),
    ("chapter-15-2.html", "Chapter 15.2 - Genuine Happiness Shines in the Hearts of Those Who Have Overcome Hardships"),
    ("chapter-15-3.html", "Chapter 15.3 - Do Not Succumb to the Eight Winds"),
    ("chapter-15-4.html", "Chapter 15.4 - There Is No Hardship We Cannot Surmount"),
    ("chapter-15-5.html", "Chapter 15.5 - Never Stop Practicing"),
    ("chapter-15-6.html", "Chapter 15.6 - Human Revolution Takes Place amid Our Struggles with Difficulties"),
    ("chapter-15-7.html", "Chapter 15.7 - Obstacles Enable Us to Polish Our Lives"),
    ("chapter-15-8.html", "Chapter 15.8 - An Impasse Is a Critical Turning Point"),
    ("chapter-15-9.html", "Chapter 15.9 - The Stronger One's Faith, the Greater One's Joy"),
    ("chapter-15-10.html", "Chapter 15.10 - Not Giving In to Doubt When Difficulties Arise"),
    ("chapter-15-11.html", "Chapter 15.11 - Difficulties Are Opportunities for Transforming Our Karma"),
    ("chapter-15-12.html", "Chapter 15.12 - A Buddha Is One Who Continues Striving"),
    ("chapter-15-13.html", "Chapter 15.13 - President Makiguchi's Noble Struggle"),
    ("chapter-15-14.html", "Chapter 15.14 - The Significance of Nichiren Daishonin's Casting Off the Transient and Revealing the True"),
    ("chapter-15-15.html", "Chapter 15.15 - The Soka Gakkai's Casting Off the Transient and Revealing the True"),
    ("chapter-15-16.html", "Chapter 15.16 - The Power to Change Poison into Medicine"),
    ("chapter-15-17.html", "Chapter 15.17 - Encouragement to Members Suffering Natural Disasters"),
    # Chapter 16
    ("chapter-16-1.html", "Chapter 16.1 - Both Buddhism and Life Are a Struggle to Be Victorious"),
    ("chapter-16-2.html", "Chapter 16.2 - Human Revolution Is a Struggle with Ourselves"),
    ("chapter-16-3.html", "Chapter 16.3 - Buddhism Originates from Shakyamuni's Triumph Over Inner Devilish Functions"),
    ("chapter-16-4.html", "Chapter 16.4 - Winning Over Ourselves Today"),
    ("chapter-16-5.html", "Chapter 16.5 - Challenge and Response"),
    ("chapter-16-6.html", "Chapter 16.6 - Stand Up with Faith Based on a Vow"),
    ("chapter-16-7.html", "Chapter 16.7 - Winning Means Refusing to Be Defeated"),
    ("chapter-16-8.html", "Chapter 16.8 - Where There Is Unseen Virtue, There Will Be Visible Reward"),
    ("chapter-16-9.html", "Chapter 16.9 - Living the Noblest Life Possible as a Human Being"),
    ("chapter-16-10.html", "Chapter 16.10 - Leading a Winning Life Based on the Mystic Law"),
    ("chapter-16-11.html", "Chapter 16.11 - Summon Up the Courage of a Lion King"),
    # Chapter 17
    ("chapter-17-1.html", "Chapter 17.1 - Leading Fulfilling Lives, Free of Regret"),
    ("chapter-17-2.html", "Chapter 17.2 - Examining the Causes and Effects That Exist in Our Lives in the Present"),
    ("chapter-17-3.html", "Chapter 17.3 - Now Is the Last Moment of One's Life"),
    ("chapter-17-4.html", "Chapter 17.4 - Every Day Is Time without Beginning"),
    ("chapter-17-5.html", "Chapter 17.5 - How We Start the Day Is the Key to Victory in Life"),
    ("chapter-17-6.html", "Chapter 17.6 - Strengthen Your Faith Day by Day and Month after Month"),
    ("chapter-17-7.html", "Chapter 17.7 - One Day of Life Is More Valuable Than All the Treasures of the Major World System"),
    # Chapter 18
    ("chapter-18-1.html", "Chapter 18.1 - Dialogue Is the Essence of Buddhism"),
    ("chapter-18-2.html", "Chapter 18.2 - Engaging in Humanistic Dialogue"),
    ("chapter-18-3.html", "Chapter 18.3 - Buddhist Dialogue Shines with the Light of Human Revolution"),
    ("chapter-18-4.html", "Chapter 18.4 - Sharing Buddhism Begins with Our Prayers for Others' Happiness"),
    ("chapter-18-5.html", "Chapter 18.5 - Perseverance and Compassion"),
    ("chapter-18-6.html", "Chapter 18.6 - The Key to Sharing Nichiren Buddhism"),
    ("chapter-18-7.html", "Chapter 18.7 - The Best Way to Benefit Others"),
    ("chapter-18-8.html", "Chapter 18.8 - The Ultimate Expression of Friendship"),
    ("chapter-18-9.html", "Chapter 18.9 - Sharing Buddhism Just as You Are"),
    ("chapter-18-10.html", "Chapter 18.10 - Confidently Sharing Our Convictions and Personal Experiences in Faith"),
    # Chapter 19
    ("chapter-19-1.html", "Chapter 19.1 - Three Key Reasons Why Buddhist Study Is Important"),
    ("chapter-19-2.html", "Chapter 19.2 - Buddhist Study to Deepen Understanding Based on Faith"),
    ("chapter-19-3.html", "Chapter 19.3 - A Shared Tradition of Studying the Writings of Nichiren Daishonin"),
    ("chapter-19-4.html", "Chapter 19.4 - Exert Yourself in the Two Ways of Practice and Study"),
    ("chapter-19-5.html", "Chapter 19.5 - Engaging in Buddhist Study Is Itself a Victory"),
    ("chapter-19-6.html", "Chapter 19.6 - A People-Centered Study Movement"),
    ("chapter-19-7.html", "Chapter 19.7 - Basing Our Lives on the Writings of Nichiren Daishonin"),
    ("chapter-19-8.html", "Chapter 19.8 - Make Study Your Foundation"),
    ("chapter-19-9.html", "Chapter 19.9 - Study of Nichiren Buddhism Is the Driving Force for Human Revolution"),
    ("chapter-19-10.html", "Chapter 19.10 - The Power of Engraving the Daishonin's Words in Our Hearts"),
    # Chapter 20
    ("chapter-20-1.html", "Chapter 20.1 - Courage, Conviction, and Hope"),
    ("chapter-20-2.html", "Chapter 20.2 - The Problems of Youth Are Themselves a Source of Light"),
    ("chapter-20-3.html", "Chapter 20.3 - You Are Each a Precious Individual with a Special Mission"),
    ("chapter-20-4.html", "Chapter 20.4 - Seeking Out Challenges for Self-Development in One's Youth"),
    ("chapter-20-5.html", "Chapter 20.5 - Always Look to the Future"),
    ("chapter-20-6.html", "Chapter 20.6 - Keep Moving Forward"),
    ("chapter-20-7.html", "Chapter 20.7 - Live with an Invincible Spirit"),
    ("chapter-20-8.html", "Chapter 20.8 - To Young Women's Division Members"),
    ("chapter-20-9.html", "Chapter 20.9 - True Happiness Is Having Good Friends"),
    ("chapter-20-10.html", "Chapter 20.10 - To Appreciate and Care for One's Parents Is the Basis of Genuine Humanity"),
    ("chapter-20-11.html", "Chapter 20.11 - Trustworthiness Is the Greatest Asset for Youth"),
    ("chapter-20-12.html", "Chapter 20.12 - Our Workplace Is an Important Stage for Our Human Revolution"),
    ("chapter-20-13.html", "Chapter 20.13 - Work and Faith Are One and Inseparable"),
    ("chapter-20-14.html", "Chapter 20.14 - Those Who Are Strong Stand Alone"),
    ("chapter-20-15.html", "Chapter 20.15 - Personal Relationships"),
    ("chapter-20-16.html", "Chapter 20.16 - Love as a Source of Growth"),
    ("chapter-20-17.html", "Chapter 20.17 - Guidance on Marriage"),
    ("chapter-20-18.html", "Chapter 20.18 - Learning Is Light, Ignorance Is Darkness"),
    ("chapter-20-19.html", "Chapter 20.19 - Be Suns Illuminating a New World"),
    ("chapter-20-20.html", "Chapter 20.20 - Cherish High Ideals"),
    ("chapter-20-21.html", "Chapter 20.21 - Ushering in a New Dawn of Human Rights"),
    ("chapter-20-22.html", "Chapter 20.22 - Youth, I'm Counting on You"),
    # Chapter 21
    ("chapter-21-1.html", "Chapter 21.1 - The Aim of Nichiren Buddhism Is Kosen-rufu"),
    ("chapter-21-2.html", "Chapter 21.2 - May Young Successors Follow on the Path of Kosen-rufu in Ever-Growing Numbers"),
    ("chapter-21-3.html", "Chapter 21.3 - Transforming the Destiny of Humanity"),
    ("chapter-21-4.html", "Chapter 21.4 - Working to Realize a Peaceful and Prosperous Society Is the Hallmark of a Living Religion"),
    ("chapter-21-5.html", "Chapter 21.5 - Kosen-rufu Is an Unending Flow"),
    ("chapter-21-6.html", "Chapter 21.6 - The Formula for Worldwide Kosen-rufu"),
    ("chapter-21-7.html", "Chapter 21.7 - Kosen-rufu Begins with One Person"),
    ("chapter-21-8.html", "Chapter 21.8 - The Soka Gakkai Is a Magnificent Realm of Inspiration and Empowerment"),
    # Chapter 22
    ("chapter-22-1.html", "Chapter 22.1 - Realizing Our Identity as Bodhisattvas of the Earth"),
    ("chapter-22-2.html", "Chapter 22.2 - Soka Gakkai Members Are the True Bodhisattvas of the Earth"),
    ("chapter-22-3.html", "Chapter 22.3 - The Virtues of the Four Leaders of the Bodhisattvas of the Earth"),
    ("chapter-22-4.html", "Chapter 22.4 - Stand-Alone Faith Infused with a Vow for Kosen-rufu"),
    ("chapter-22-5.html", "Chapter 22.5 - This Is My Vow, and I Will Never Forsake It"),
    ("chapter-22-6.html", "Chapter 22.6 - Action Is the Hallmark of Practitioners of Nichiren Buddhism"),
    ("chapter-22-7.html", "Chapter 22.7 - Awakening People to Their Mission as Bodhisattvas of the Earth"),
    # Chapter 23
    ("chapter-23-1.html", "Chapter 23.1 - The Aim of Kosen-rufu Is the Happiness of Each Person"),
    ("chapter-23-2.html", "Chapter 23.2 - Everyone Has a Mission"),
    ("chapter-23-3.html", "Chapter 23.3 - Treasuring Each Individual Is the Spirit of the Buddha"),
    ("chapter-23-4.html", "Chapter 23.4 - Each Person's Life Is a Treasure Tower As Vast As the Universe"),
    ("chapter-23-5.html", "Chapter 23.5 - All Are Supremely Worthy"),
    ("chapter-23-6.html", "Chapter 23.6 - Treasuring Those Striving Hard behind the Scenes"),
    ("chapter-23-7.html", "Chapter 23.7 - Empathy Is the Essence of the Soka Gakkai Spirit"),
    ("chapter-23-8.html", "Chapter 23.8 - Nichiren Buddhism Is a Teaching of Unparalleled Humanism"),
    ("chapter-23-9.html", "Chapter 23.9 - President Makiguchi Treasured Each Individual"),
    ("chapter-23-10.html", "Chapter 23.10 - Working among and with the People"),
    ("chapter-23-11.html", "Chapter 23.11 - President Toda's Commitment to Personal Guidance"),
    ("chapter-23-12.html", "Chapter 23.12 - The Tradition of the Soka Gakkai"),
    ("chapter-23-13.html", "Chapter 23.13 - Important Points for Offering Personal Guidance"),
    ("chapter-23-14.html", "Chapter 23.14 - The Key to the Soka Gakkai's Development"),
    # Chapter 24
    ("chapter-24-1.html", "Chapter 24.1 - Advancing with Good Friends Is All of Buddhist Practice"),
    ("chapter-24-2.html", "Chapter 24.2 - The Soka Gakkai Is a Gathering of Good Friends"),
    ("chapter-24-3.html", "Chapter 24.3 - The Organization Exists for People's Happiness"),
    ("chapter-24-4.html", "Chapter 24.4 - Expanding Our Life State"),
    ("chapter-24-5.html", "Chapter 24.5 - Creating a United Network of People Dedicated to Good"),
    ("chapter-24-6.html", "Chapter 24.6 - Discussion Meetings Are the Heart of the Soka Gakkai"),
    ("chapter-24-7.html", "Chapter 24.7 - Kosen-rufu Starts from Discussion Meetings"),
    ("chapter-24-8.html", "Chapter 24.8 - The Beautiful Realm of the Soka Family"),
    ("chapter-24-9.html", "Chapter 24.9 - What Is Soka Gakkai Buddha"),
    ("chapter-24-10.html", "Chapter 24.10 - Ensuring That the Soka Gakkai Endures"),
    # Chapter 25
    ("chapter-25-1.html", "Chapter 25.1 - The Unity of Many in Body, One in Mind Is the True Picture of Kosen-rufu"),
    ("chapter-25-2.html", "Chapter 25.2 - What Is the Meaning of Many in Body, One in Mind"),
    ("chapter-25-3.html", "Chapter 25.3 - Showing One Another the Same Respect As We Would a Buddha"),
    ("chapter-25-4.html", "Chapter 25.4 - Unity That Embraces Diversity"),
    ("chapter-25-5.html", "Chapter 25.5 - The Treasure of Harmonious Unity"),
    ("chapter-25-6.html", "Chapter 25.6 - Unity of Purpose Is the Key to Achieving Our Goals"),
    ("chapter-25-7.html", "Chapter 25.7 - One in Mind Means Sharing an Unwavering Commitment in Faith"),
    ("chapter-25-8.html", "Chapter 25.8 - Self-Reliant Faith Is the Foundation of Unity"),
    ("chapter-25-9.html", "Chapter 25.9 - The Fundamental Spirit of the Soka Gakkai"),
    ("chapter-25-10.html", "Chapter 25.10 - The Power to Unite Humanity"),
    # Chapter 26
    ("chapter-26-1.html", "Chapter 26.1 - A Leadership Revolution"),
    ("chapter-26-2.html", "Chapter 26.2 - Have a Big Heart"),
    ("chapter-26-3.html", "Chapter 26.3 - Lead by Example"),
    ("chapter-26-4.html", "Chapter 26.4 - Winning People's Trust through Compassion and Wisdom"),
    ("chapter-26-5.html", "Chapter 26.5 - The Organization Hinges on Its Leaders"),
    ("chapter-26-6.html", "Chapter 26.6 - The Significance of Soka Gakkai Leadership Positions"),
    ("chapter-26-7.html", "Chapter 26.7 - Living with Energy and Vigor"),
    ("chapter-26-8.html", "Chapter 26.8 - Finding and Fostering Capable Individuals"),
    ("chapter-26-9.html", "Chapter 26.9 - What Defines a Capable Person in the Soka Gakkai"),
    ("chapter-26-10.html", "Chapter 26.10 - One Person of Passionate Commitment Is Stronger Than a Force of Untold Numbers"),
    ("chapter-26-11.html", "Chapter 26.11 - Leadership Positions in the Soka Gakkai Are Positions of Responsibility"),
    ("chapter-26-12.html", "Chapter 26.12 - The Foremost Message of the Buddha"),
    # Chapter 27
    ("chapter-27-1.html", "Chapter 27.1 - The Mentor-Disciple Relationship Is a Sublime Spiritual Relay"),
    ("chapter-27-2.html", "Chapter 27.2 - Mentor and Disciple Are Like a Needle and Thread"),
    ("chapter-27-3.html", "Chapter 27.3 - The 10 Major Disciples of Shakyamuni"),
    ("chapter-27-4.html", "Chapter 27.4 - The Mentor-Disciple Relationship Is the Cornerstone of Nichiren Buddhism"),
    ("chapter-27-5.html", "Chapter 27.5 - Walking the Path of a Disciple throughout One's Life"),
    ("chapter-27-6.html", "Chapter 27.6 - What Defines a Good Teacher in Buddhism"),
    ("chapter-27-7.html", "Chapter 27.7 - Having a Mentor in One's Heart"),
    ("chapter-27-8.html", "Chapter 27.8 - The Disciples Are Key"),
    # Chapter 28
    ("chapter-28-1.html", "Chapter 28.1 - The Strength and Kindness of President Makiguchi"),
    ("chapter-28-2.html", "Chapter 28.2 - An Indescribable Joy"),
    ("chapter-28-3.html", "Chapter 28.3 - The Soka Gakkai's Founding Spirit"),
    ("chapter-28-4.html", "Chapter 28.4 - The Soka Gakkai's Founding and the Mentor-Disciple Spirit"),
    ("chapter-28-5.html", "Chapter 28.5 - President Makiguchi's Lifelong Struggle"),
    ("chapter-28-6.html", "Chapter 28.6 - Raising High the Banner of Kosen-rufu"),
    ("chapter-28-7.html", "Chapter 28.7 - The Immortal Struggles of Presidents Makiguchi and Toda"),
    ("chapter-28-8.html", "Chapter 28.8 - Actualizing the Vision of the First and Second Presidents"),
    ("chapter-28-9.html", "Chapter 28.9 - Describing My Mentor, Josei Toda"),
    ("chapter-28-10.html", "Chapter 28.10 - My First Encounter with President Toda"),
    ("chapter-28-11.html", "Chapter 28.11 - My Training at Toda University"),
    ("chapter-28-12.html", "Chapter 28.12 - Opening the Way for Mr. Toda's Presidency"),
    ("chapter-28-13.html", "Chapter 28.13 - The Oneness of Mentor and Disciple Is the Life of Nichiren Buddhism"),
    ("chapter-28-14.html", "Chapter 28.14 - Reporting Victory to One's Mentor"),
    ("chapter-28-15.html", "Chapter 28.15 - Disciples Taking Full Responsibility for Kosen-rufu"),
    ("chapter-28-16.html", "Chapter 28.16 - July 3—A Solemn Day of Mentor and Disciple"),
    ("chapter-28-17.html", "Chapter 28.17 - An Indomitable Struggle for Human Rights"),
    ("chapter-28-18.html", "Chapter 28.18 - March 16—An Eternal Ceremony of Mentor and Disciple"),
    ("chapter-28-19.html", "Chapter 28.19 - April 2—Remembering My Mentor, Josei Toda"),
    ("chapter-28-20.html", "Chapter 28.20 - Becoming Third Soka Gakkai President"),
    ("chapter-28-21.html", "Chapter 28.21 - Taking the Lead in Kosen-rufu throughout Eternity"),
    ("chapter-28-22.html", "Chapter 28.22 - Writing The Human Revolution"),
    ("chapter-28-23.html", "Chapter 28.23 - A Chronicle of My Mentor's Greatness"),
    ("chapter-28-24.html", "Chapter 28.24 - On the Completion of The New Human Revolution"),
    ("chapter-28-25.html", "Chapter 28.25 - Realizing My Mentor's Vision"),
    ("chapter-28-26.html", "Chapter 28.26 - Carrying the Founding Spirit into the Future"),
    ("chapter-28-27.html", "Chapter 28.27 - The Eternal Story of Soka Mentors and Disciples"),
    # Chapter 29
    ("chapter-29-1.html", "Chapter 29.1 - The Soka Gakkai Is a Humanistic Movement"),
    ("chapter-29-2.html", "Chapter 29.2 - The Soka Gakkai's Spiritual Independence—A Fresh Start toward Worldwide Kosen-rufu"),
    ("chapter-29-3.html", "Chapter 29.3 - The Dawn of a Religious Revolution"),
    ("chapter-29-4.html", "Chapter 29.4 - The Spirit of Working for the Happiness of the People"),
    ("chapter-29-5.html", "Chapter 29.5 - At the Forefront of Religious Reform"),
    ("chapter-29-6.html", "Chapter 29.6 - Responding Wisely to the Times"),
    ("chapter-29-7.html", "Chapter 29.7 - Embracing Others in Friendship with a Big, Magnanimous Heart"),
    ("chapter-29-8.html", "Chapter 29.8 - Buddhism Teaches a Path of Life and Humanity"),
    # Chapter 30
    ("chapter-30-1.html", "Chapter 30.1 - Aiming toward the Soka Gakkai's Centennial with the Future Division"),
    ("chapter-30-2.html", "Chapter 30.2 - Treasuring the Emissaries from the Future"),
    ("chapter-30-3.html", "Chapter 30.3 - What Should We Pass On to the Future Division"),
    ("chapter-30-4.html", "Chapter 30.4 - Be Good Friends to the Future Division Members"),
    ("chapter-30-5.html", "Chapter 30.5 - The Seven Guidelines for the Future Division"),
    ("chapter-30-6.html", "Chapter 30.6 - Life Itself Is a Treasure"),
    ("chapter-30-7.html", "Chapter 30.7 - Passing On Faith to the Next Generation"),
    ("chapter-30-8.html", "Chapter 30.8 - Children Are Our Treasures"),
    ("chapter-30-9.html", "Chapter 30.9 - Fostering Successors Who Will Surpass Us"),
    ("chapter-30-10.html", "Chapter 30.10 - The Growth of Future Division Members Holds the Key to Victory"),
    ("chapter-30-11.html", "Chapter 30.11 - Toward the Soka Gakkai's 200th Anniversary"),
    # Chapter 31
    ("chapter-31-1.html", "Chapter 31.1 - Pioneers in a Grand Experiment"),
    ("chapter-31-2.html", "Chapter 31.2 - Treasure Towers of Respect for the Dignity of Life"),
    ("chapter-31-3.html", "Chapter 31.3 - Creating a World without War"),
    ("chapter-31-4.html", "Chapter 31.4 - A New Humanism"),
    ("chapter-31-5.html", "Chapter 31.5 - The Century of Life"),
    ("chapter-31-6.html", "Chapter 31.6 - Placing the Focus on Human Beings"),
    ("chapter-31-7.html", "Chapter 31.7 - Respecting the Dignity of All People"),
    ("chapter-31-8.html", "Chapter 31.8 - A Realm of Boundless Inspiration"),
    ("chapter-31-9.html", "Chapter 31.9 - A University without Walls"),
    ("chapter-31-10.html", "Chapter 31.10 - Education: The Foundation for Peace"),
    ("chapter-31-11.html", "Chapter 31.11 - Our Legacy to Humanity"),
    ("chapter-31-12.html", "Chapter 31.12 - Kosen-rufu Is a Great Cultural Movement"),
    ("chapter-31-13.html", "Chapter 31.13 - The Power of Art to Bring People Together"),
    ("chapter-31-14.html", "Chapter 31.14 - Restoring the Poetic Spirit"),
    ("chapter-31-15.html", "Chapter 31.15 - Photography Is a Universal Language"),
    ("chapter-31-16.html", "Chapter 31.16 - Reviving the Culture of the Written Word"),
    ("chapter-31-17.html", "Chapter 31.17 - A Humanistic Newspaper—the Seikyo Shimbun"),
    ("chapter-31-18.html", "Chapter 31.18 - Making Art Available to All"),
    ("chapter-31-19.html", "Chapter 31.19 - Bringing the World Together through Culture"),
    ("chapter-31-20.html", "Chapter 31.20 - The Epitome of Human Harmony"),
    ("chapter-31-21.html", "Chapter 31.21 - Nothing Is More Barbarous Than War"),
    ("chapter-31-22.html", "Chapter 31.22 - The Starting Point of the Soka Gakkai's Peace Activities—The Declaration Calling for the Abolition of Nuclear Weapons"),
    ("chapter-31-23.html", "Chapter 31.23 - Inner Transformation Is the Key"),
    ("chapter-31-24.html", "Chapter 31.24 - Conflict Arises from the Anger in Our Hearts"),
    ("chapter-31-25.html", "Chapter 31.25 - The Power to Overcome the Threat of Nuclear Weapons"),
    ("chapter-31-26.html", "Chapter 31.26 - Dialogue Is the Sure and Certain Path to Peace"),
    ("chapter-31-27.html", "Chapter 31.27 - Choosing Dialogue"),
    ("chapter-31-28.html", "Chapter 31.28 - The Wisdom for Interfaith Dialogue"),
    ("chapter-31-29.html", "Chapter 31.29 - An Age of Humanitarian Competition"),
    ("chapter-31-30.html", "Chapter 31.30 - The 21st Century Is the Century of Africa"),
    ("chapter-31-31.html", "Chapter 31.31 - Building a Culture of Peace through the Power of Women"),
    ("chapter-31-32.html", "Chapter 31.32 - Toward a Sustainable Global Society"),
    # Conclusion
    ("conclusion-1.html", "Conclusion 1 - A New Series of Seven Bells toward the Year 2050"),
    ("conclusion-2.html", "Conclusion 2 - Determinations for the Future into the 23rd Century"),
    ("conclusion-3.html", "Conclusion 3 - Making Respect for the Dignity of Life the Spirit of the 21st Century"),
    ("conclusion-4.html", "Conclusion 4 - Standing Always on the Side of the People"),
    ("conclusion-5.html", "Conclusion 5 - The Soka Gakkai Will Always Open a Way Forward"),
    ("conclusion-6.html", "Conclusion 6 - Forever Connected by Our Great Vow for Kosen-rufu"),
    ("conclusion-7.html", "Conclusion 7 - Make Your Life a Beacon"),
]


def clean_text(text):
    """Clean and format text content"""
    # Remove extra whitespace
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    return '\n\n'.join(cleaned_lines)


def fetch_chapter(url, title):
    """Fetch a chapter and return its text content"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content area
        # This may need adjustment based on the actual HTML structure
        content = soup.find('div', class_='field-item')
        if not content:
            content = soup.find('article')
        if not content:
            content = soup.find('main')

        if content:
            # Remove script and style elements
            for script in content(["script", "style", "nav", "header", "footer"]):
                script.decompose()

            text = content.get_text()
            return clean_text(text)
        else:
            return f"Could not find content for {title}"

    except Exception as e:
        return f"Error fetching {title}: {str(e)}"


def save_chapter(directory, filename, title, content):
    """Save chapter content to a text file"""
    filepath = os.path.join(directory, filename.replace('.html', '.txt'))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"{title}\n")
        f.write("=" * len(title) + "\n\n")
        f.write(content)
    return filepath


def main():
    """Main function to collect all chapters"""
    base_path = "/Users/bonganimlambo/Documents/Code Development/Projects/Buddhist-Study-Materials"
    book1_dir = os.path.join(base_path, "01-The-Wisdom-for-Creating-Happiness-and-Peace")

    print(f"Starting collection of {len(BOOK1_CHAPTERS)} chapters...")
    print(f"Saving to: {book1_dir}")

    success_count = 0
    error_count = 0

    for i, (filename, title) in enumerate(BOOK1_CHAPTERS, 1):
        url = f"{BASE_URL}/resources/study-materials/buddhist-study/the-wisdom-for-creating-happiness-and-peace/{filename}"

        print(f"[{i}/{len(BOOK1_CHAPTERS)}] Fetching: {title}")

        content = fetch_chapter(url, title)

        if content.startswith("Error") or content.startswith("Could not"):
            print(f"  ❌ Failed: {content}")
            error_count += 1
        else:
            filepath = save_chapter(book1_dir, filename, title, content)
            print(f"  ✓ Saved: {os.path.basename(filepath)}")
            success_count += 1

        # Be respectful to the server
        time.sleep(1)

    print(f"\n{'='*60}")
    print(f"Collection complete!")
    print(f"Successful: {success_count}")
    print(f"Errors: {error_count}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
