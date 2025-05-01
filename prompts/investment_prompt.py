from langchain_core.prompts import ChatPromptTemplate


def get_explanation_prompt():
    return ChatPromptTemplate.from_template(
        """
        You are an investment banking analyst reviewing the following financial summary:

        {summary}

        The initial investment recommendation is:

        {recommendation}

        Write a professional analysis that includes:
        - 📈 A **Bullish Case** (reasons to be optimistic based on the data)
        - 📉 A **Bearish Case** (risks or cautionary signs based on the data)
        - ✅ List 2-3 Strengths
        - ⚠️ List 2-3 Risks
        - 🎯 Conclude with an **Investment Score out of 10** and final recommendation tone (Buy / Hold / Sell).

        Keep the tone formal but actionable, as if preparing a client-facing memo.

        Format the result into an inline object as follows:
        {{
            bullish: <bullish case>,
            bearish: <bearish case>,
            recommendation: <recommendation with HTML formatting>,
            investment_score: <score out of 10>
        }}
        """
    )
