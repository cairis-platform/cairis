<?xml version='1.0'?>
<!-- $URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/config/iris_stylesheet.xsl $ $Id: iris_stylesheet.xsl 61 2009-08-30 20:25:53Z shaf $ -->
<xsl:stylesheet
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
     xmlns:fo="http://www.w3.org/1999/XSL/Format"
     xmlns:fox="http://xml.apache.org/fop/extensions"
     version="1.0">

<xsl:import href="http://docbook.sourceforge.net/release/xsl/current/fo/docbook.xsl"/>


<!-- We aren't in the US -->
<xsl:param name="paper.type" select="'A4'"/>

<!-- We're using FOP -->
<xsl:param name="fop.extensions" select="'1'"/>

<!-- Number the sections -->
<xsl:param name="section.autolabel" select="'1'"/>

<!-- Don't restart section numbers when we hit a new chapter -->
<xsl:param name="section.label.includes.component.label" select="1"/>

<xsl:param name="xref.with.number.and.title" select="0"/>

<!-- adjust margins -->
<xsl:param name="title.margin.left" select="'-3pc'"/>
<xsl:param name="body.margin.bottom" select="'1.1in'"/>
<xsl:param name="page.margin.bottom" select="'0.3in'"/>
<xsl:param name="page.margin.top" select="'9mm'"/>
<xsl:param name="body.margin.top" select="'25mm'"/>
<!-- allow space for headers/footers -->
<xsl:param name="region.before.extent" select="'53pt'"/>
<xsl:param name="region.after.extent" select="'1.0in'"/>

<!-- configure fonts -->
<xsl:param name="title.font.family" select="'serif'"/>
<xsl:param name="body.font.size" select="'12pt'"/>
<xsl:attribute-set name="header.content.properties">
  <xsl:attribute name="font-family">Helvetica</xsl:attribute>
  <xsl:attribute name="font-size">9pt</xsl:attribute>
</xsl:attribute-set>
<xsl:attribute-set name="monospace.verbatim.properties">
  <xsl:attribute name="font-size">10pt</xsl:attribute>
</xsl:attribute-set>

<!-- The chapter and appendix headings are way to big, so ensure it is only 12 pt -->
<xsl:template match="title" mode="set.titlepage.recto.auto.mode">
  <fo:block xsl:use-attribute-sets="set.titlepage.recto.style"
      text-align="center" font-size="12pt" space-before="18.6624pt"
      font-weight="bold" font-family="{$title.fontset}">
  <xsl:call-template name="division.title">
    <xsl:with-param name="node" select="ancestor-or-self::set[1]"/>
  </xsl:call-template>
</fo:block>
</xsl:template>

<xsl:template match="title" mode="chapter.titlepage.recto.auto.mode">
  <!-- adding the id of the chapter to this block is a nasty hack around a
  bug in FOP: the id is on the fo:page-sequence and so the page numbers and
  links don't work. This is especially nasty because the id gets duplicated -->
  <xsl:variable name="id">
    <xsl:call-template name="object.id">
      <xsl:with-param name="object" select=".."/>
    </xsl:call-template>
  </xsl:variable>
  <fo:block id="{$id}" xsl:use-attribute-sets="chapter.titlepage.recto.style"
      font-size="12pt" font-weight="bold">
    <xsl:call-template name="component.title">
      <xsl:with-param name="node" select="ancestor-or-self::chapter[1]"/>
    </xsl:call-template>
  </fo:block>
</xsl:template>

<xsl:template match="title" mode="appendix.titlepage.recto.auto.mode">
  <fo:block xsl:use-attribute-sets="appendix.titlepage.recto.style"
      font-size="12pt" font-weight="bold">
    <xsl:call-template name="component.title">
      <xsl:with-param name="node" select="ancestor-or-self::appendix[1]"/>
    </xsl:call-template>
  </fo:block>
</xsl:template>

<xsl:attribute-set name="titlepage.title.level1.properties">
  <xsl:attribute name="space-before.minimum">1em</xsl:attribute>
  <xsl:attribute name="space-before.optimum">1.5em</xsl:attribute>
  <xsl:attribute name="space-before.maximum">2em</xsl:attribute>
  <xsl:attribute name="space-after">0.5em</xsl:attribute>
  <xsl:attribute name="font-size">12pt</xsl:attribute>
  <xsl:attribute name="font-weight">bold</xsl:attribute>
  <xsl:attribute name="font-family"><xsl:value-of select="$title.font.family"/></xsl:attribute>
  <xsl:attribute name="text-align">center</xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="titlepage.department.properties">
  <xsl:attribute name="font-size">12pt</xsl:attribute>
  <xsl:attribute name="font-weight">bold</xsl:attribute>
  <xsl:attribute name="font-family"><xsl:value-of select="$title.font.family"/></xsl:attribute>
  <xsl:attribute name="text-align">center</xsl:attribute>
</xsl:attribute-set>

<!-- Ditto for the section headings -->
<xsl:attribute-set name="section.title.level1.properties">
  <xsl:attribute name="font-size">12pt</xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="section.title.level2.properties">
  <xsl:attribute name="font-size">12pt</xsl:attribute>
  <xsl:attribute name="font-weight">normal</xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="section.title.level3.properties">
  <xsl:attribute name="font-size">12pt</xsl:attribute>
  <xsl:attribute name="font-weight">normal</xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="section.title.level4.properties">
  <xsl:attribute name="font-size">12pt</xsl:attribute>
  <xsl:attribute name="font-weight">normal</xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="section.title.level5.properties">
  <xsl:attribute name="font-size">12pt</xsl:attribute>
  <xsl:attribute name="font-weight">normal</xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="section.title.level6.properties">
  <xsl:attribute name="font-size">12pt</xsl:attribute>
  <xsl:attribute name="font-weight">normal</xsl:attribute>
</xsl:attribute-set>

<!-- Sometimes, forcing a page-break is handy in the document -->
<xsl:template match="processing-instruction('hard-pagebreak')">
  <fo:block break-before='page'/>
</xsl:template>

<xsl:variable name="subsystem">
  <xsl:text>Infrastructure </xsl:text>
  <xsl:choose>
    <xsl:when test="substring-before(substring-after(substring-after(/book/bookinfo/biblioid,'-'),'-'),'-') = 'FDIH'">
      <xsl:text>Hardware</xsl:text>
    </xsl:when>
    <xsl:otherwise>Software</xsl:otherwise>
  </xsl:choose>
</xsl:variable>

<xsl:template name="header.table">
  <xsl:param name="pageclass" select="''"/>
  <xsl:param name="sequence" select="''"/>
  <xsl:param name="gentext-key" select="''"/>

  <!-- Really output a header? -->
  <xsl:choose>
    <xsl:when test="$pageclass = 'titlepage' and $gentext-key = 'book'
                    and $sequence='first'">
      <fo:block>
        <fo:external-graphic>
          <xsl:attribute name="src">
            <xsl:call-template name="fo-external-image">
              <xsl:with-param name="filename" select="concat(/home/irisuser/iris, '/iris/images/oxBrand.pdf')"/>
            </xsl:call-template>
          </xsl:attribute>
        </fo:external-graphic>
      </fo:block>
    </xsl:when>
    <xsl:otherwise>
      <fo:table margin-right="-3pc" table-layout="fixed" width="100%">
        <!-- <xsl:call-template name="head.sep.rule"/> -->
        <fo:table-column column-number="1" column-width="1in"/>
        <fo:table-column column-number="2"/>
        <fo:table-column column-number="3" column-width="10mm"/>
        <fo:table-column column-number="4" column-width="6mm"/>
        <fo:table-body>
          <fo:table-row>
            <fo:table-cell>
              <fo:block>Doc. Title:</fo:block>
            </fo:table-cell>
            <fo:table-cell>
              <fo:block>
                <xsl:text>Flight Dynamics </xsl:text>
                <xsl:value-of select="$subsystem"/>
              </fo:block>
            </fo:table-cell>
            <fo:table-cell>
              <fo:block>Issue:</fo:block>
            </fo:table-cell>
            <fo:table-cell text-align="right">
              <fo:block>
                <xsl:value-of select="substring-before(/book/bookinfo/edition,'.')"/>
              </fo:block>
            </fo:table-cell>
          </fo:table-row>
          <fo:table-row>
            <fo:table-cell><fo:block/></fo:table-cell>
            <fo:table-cell>
              <fo:block><xsl:value-of select="/book/title" /></fo:block>
            </fo:table-cell>
            <fo:table-cell>
              <fo:block>Rev:</fo:block>
            </fo:table-cell>
            <fo:table-cell text-align="right">
              <fo:block>
                <xsl:value-of select="substring-after(string(/book/bookinfo/edition),'.')" />
              </fo:block>
            </fo:table-cell>
          </fo:table-row>
          <fo:table-row>
            <fo:table-cell>
              <fo:block>Doc. Ref:</fo:block>
            </fo:table-cell>
            <fo:table-cell>
              <fo:block><xsl:value-of select="/book/bookinfo/biblioid"/></fo:block>
            </fo:table-cell>
          </fo:table-row>
          <fo:table-row>
            <fo:table-cell>
              <fo:block>Date:</fo:block>
            </fo:table-cell>
            <fo:table-cell>
              <fo:block><xsl:value-of select="/book/bookinfo/date"/></fo:block>
            </fo:table-cell>
            <fo:table-cell>
              <fo:block>Page:</fo:block>
            </fo:table-cell>
            <fo:table-cell text-align="right">
              <fo:block><fo:page-number/></fo:block>
            </fo:table-cell>
          </fo:table-row>
        </fo:table-body>
      </fo:table>
      <fo:leader
          leader-length="{$page.width} - {$page.margin.inner} - {$page.margin.outer} - 2 * {$title.margin.left}"
          leader-pattern="rule" rule-thickness="0.5pt"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="footer.table">
  <fo:table table-layout="fixed" width="100%">
    <fo:table-column column-number="1" column-width="44mm"/>
    <fo:table-column column-number="2"/>
    <fo:table-body>
      <fo:table-row>
        <fo:table-cell display-align="after" text-align="right">
          <fo:block margin-right="-{$title.margin.left}" font-family="ESAtitle" font-size="5pt">European Space Agency</fo:block>
          <fo:block margin-right="-{$title.margin.left}" font-family="ESAtitle" font-size="5pt">Agence spatiale europ&#233;enne</fo:block>
        </fo:table-cell>
        <fo:table-cell><fo:block/></fo:table-cell>
      </fo:table-row>
      <fo:table-row>
        <fo:table-cell><fo:block/></fo:table-cell>
        <fo:table-cell display-align="after">
          <fo:block margin-left="{$title.margin.left}" font-family="ESAtitle" font-size="20pt">ESOC</fo:block>
          <fo:block margin-left="{$title.margin.left}" font-family="FuturaTMedCon" font-size="10pt">Robert-Bosch-Strasse 5, 64293 Darmstadt, Germany</fo:block>
          <fo:block margin-left="{$title.margin.left}" font-family="FuturaTMedCon" font-size="10pt">Tel. +49 (0) 6151 90 0 - Fax +49 (0) 6151 90 495</fo:block>
        </fo:table-cell>
      </fo:table-row>
    </fo:table-body>
  </fo:table>
</xsl:template>

<!-- our top-level chapters are just sections -->
<xsl:param name="local.l10n.xml" select="document('')"/>
<l:i18n xmlns:l="http://docbook.sourceforge.net/xmlns/l10n/1.0">
  <l:l10n xmlns:l="http://docbook.sourceforge.net/xmlns/l10n/1.0" language="en">
   <l:context name="title">
      <l:template name="chapter" text="%n.&#160;%t"/>
    </l:context>
   <l:context name="title-numbered">
      <l:template name="chapter" text="%n.&#160;%t"/>
   </l:context>
  </l:l10n>
</l:i18n>

<xsl:template match="edition" mode="titlepage.mode">
  <xsl:text>Issue </xsl:text>
  <xsl:value-of select="."/>
</xsl:template>

<xsl:template name="book.titlepage">
  <fo:block>
    <fo:block xsl:use-attribute-sets="titlepage.department.properties">
      <xsl:text>University of Oxford</xsl:text>
    </fo:block>
    <fo:block xsl:use-attribute-sets="titlepage.department.properties">
      <xsl:text>Computing Laboratory</xsl:text>
    </fo:block>
    <!-- FOP doesn't appear to support double lines -->
    <fo:block space-before="41mm" border-left-style="solid" border-right-style="solid"
        border-top-style="solid" border-bottom-style="solid" border-left-width="0.5pt"
        border-right-width="0.5pt" border-top-width="0.5pt" border-bottom-width="0.5pt"
        padding-before="2pt" padding-after="2pt" padding-left="2pt" padding-right="2pt"
        margin-left="50mm - {$page.margin.inner}" margin-right="50mm - {$page.margin.inner}">
      <fo:block border-left-style="solid" border-right-style="solid"
          border-top-style="solid" border-bottom-style="solid" border-left-width="0.5pt"
          border-right-width="0.5pt" border-top-width="0.5pt" border-bottom-width="0.5pt"
          padding-before="3mm" padding-after="3mm">
        <xsl:call-template name="titlepage.title">
          <xsl:with-param name="title" select="'Flight Dynamics'"/>
        </xsl:call-template>
        <xsl:call-template name="titlepage.title">
          <xsl:with-param name="title" select="$subsystem"/>
        </xsl:call-template>
        <xsl:call-template name="titlepage.title"/>
        <xsl:apply-templates mode="book.titlepage.recto.auto.mode" select="bookinfo/biblioid"/>
        <xsl:apply-templates mode="book.titlepage.recto.auto.mode" select="bookinfo/revision"/>
        <xsl:apply-templates mode="book.titlepage.recto.auto.mode" select="bookinfo/edition"/>
        <xsl:apply-templates mode="book.titlepage.recto.auto.mode" select="bookinfo/date"/>
      </fo:block>
    </fo:block>
    <xsl:if test="bookinfo/revhistory">
      <fo:block break-before="page">
        <xsl:apply-templates mode="book.titlepage.verso.auto.mode" select="bookinfo/revhistory"/>
      </fo:block>
    </xsl:if>
    <xsl:if test="bookinfo/authorgroup">
      <fo:block break-before="page">
        <xsl:apply-templates mode="book.approval" select="bookinfo/authorgroup"/>
      </fo:block>
    </xsl:if>
    <xsl:if test="bookinfo/abstract">
      <fo:block id="idAbstract" break-before="page" xsl:use-attribute-sets="titlepage.title.level1.properties">
        <xsl:text>Abstract</xsl:text>
      </fo:block>
      <xsl:apply-templates mode="book.titlepage.verso.auto.mode" select="bookinfo/abstract"/>
    </xsl:if>
  </fo:block>
</xsl:template>

<xsl:template name="titlepage.title">
  <xsl:param name="title" select="title"/>
  <fo:block xsl:use-attribute-sets="book.titlepage.recto.style" text-align="center"
      font-size="14pt" space-after="9mm" font-weight="bold" font-family="{$title.font.family}">
    <xsl:value-of select="$title"/>
  </fo:block>
</xsl:template>

<xsl:template match="biblioid" mode="book.titlepage.recto.auto.mode">
  <fo:block xsl:use-attribute-sets="book.titlepage.recto.style" font-size="12pt"
      space-after="9mm" keep-with-next="always">
    <xsl:apply-templates select="." mode="titlepage.mode"/>
  </fo:block>
</xsl:template>

<xsl:template match="revision" mode="book.titlepage.recto.auto.mode">
  <fo:block xsl:use-attribute-sets="book.titlepage.recto.style"
      font-size="12pt" space-after="9mm">
    <xsl:apply-templates select="." mode="book.titlepage.recto.mode"/>
  </fo:block>
</xsl:template>

<xsl:template match="edition" mode="book.titlepage.recto.auto.mode">
  <fo:block xsl:use-attribute-sets="book.titlepage.recto.style"
      font-size="12pt" space-after="9mm">
    <xsl:apply-templates select="." mode="titlepage.mode"/>
  </fo:block>
</xsl:template>

<xsl:template match="date" mode="book.titlepage.recto.auto.mode">
  <fo:block xsl:use-attribute-sets="book.titlepage.recto.style"
      font-size="12pt">
    <xsl:apply-templates select="." mode="titlepage.mode"/>
  </fo:block>
</xsl:template>

<xsl:template match="revhistory" mode="book.titlepage.verso.auto.mode">
  <fo:block xsl:use-attribute-sets="book.titlepage.verso.style" space-before="0.5em">
    <xsl:apply-templates select="." mode="titlepage.mode"/>
  </fo:block>
</xsl:template>

<xsl:template match="abstract" mode="book.titlepage.verso.auto.mode">
  <fo:block xsl:use-attribute-sets="book.titlepage.verso.style" space-before="0.5em"
      text-align="start" margin-left="0.5in" margin-right="0.5in"
      font-family="{$body.font.family}" font-size="{$body.font.size}">
    <xsl:apply-templates select="." mode="titlepage.mode"/>
  </fo:block>
</xsl:template>

<xsl:template name="table-cell">
  <xsl:param name="string"/>

  <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
    <xsl:call-template name="border">
      <xsl:with-param name="side" select="'bottom'"/>
    </xsl:call-template>
    <xsl:call-template name="border">
      <xsl:with-param name="side" select="'right'"/>
    </xsl:call-template>
    <fo:block font-weight="bold">
      <xsl:value-of select="$string"/>
    </fo:block>
  </fo:table-cell>
</xsl:template>

<xsl:template match="author" mode="book.approval">
  <fo:table-row>
    <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'bottom'"/>
      </xsl:call-template>
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'right'"/>
      </xsl:call-template>
      <fo:block>
        <xsl:value-of select="firstname"/>
        <xsl:text> </xsl:text>
        <xsl:value-of select="surname"/>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'bottom'"/>
      </xsl:call-template>
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'right'"/>
      </xsl:call-template>
      <fo:block><xsl:value-of select="affiliation"/></fo:block>
    </fo:table-cell>
    <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'bottom'"/>
      </xsl:call-template>
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'right'"/>
      </xsl:call-template>
      <fo:block font-weight="100">
        <xsl:if test="$original = ''">
          <xsl:text>Signed on original</xsl:text>
        </xsl:if>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'bottom'"/>
      </xsl:call-template>
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'right'"/>
      </xsl:call-template>
      <fo:block/>
    </fo:table-cell>
  </fo:table-row>
</xsl:template>

<xsl:template match="author" mode="book.distrib">
  <fo:table-row>
    <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'bottom'"/>
      </xsl:call-template>
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'right'"/>
      </xsl:call-template>
      <fo:block><xsl:value-of select="affiliation"/></fo:block>
    </fo:table-cell>
    <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'bottom'"/>
      </xsl:call-template>
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'right'"/>
      </xsl:call-template>
      <fo:block>
        <xsl:value-of select="firstname"/>
        <xsl:text> </xsl:text>
        <xsl:value-of select="surname"/>
        <xsl:for-each select="following-sibling::author[affiliation = current()/affiliation]">
          <xsl:text>, </xsl:text>
          <xsl:value-of select="firstname"/>
          <xsl:text> </xsl:text>
          <xsl:value-of select="surname"/>
        </xsl:for-each>
      </fo:block>
    </fo:table-cell>
  </fo:table-row>
</xsl:template>

<xsl:template match="authorgroup" mode="book.approval">
  <fo:block id="idDocApp" xsl:use-attribute-sets="titlepage.title.level1.properties">
    <xsl:text>Document Approval</xsl:text>
  </fo:block>
  <xsl:if test="author[not(@role)]">
    <fo:table width="100%" border-collapse="collapse" xsl:use-attribute-sets="informal.object.properties">
      <xsl:call-template name="table.frame"/>
      <fo:table-column column-number="1" column-width="proportional-column-width(1)"/>
      <fo:table-column column-number="2" column-width="proportional-column-width(1)"/>
      <fo:table-column column-number="3" column-width="proportional-column-width(1)"/>
      <fo:table-column column-number="4" column-width="proportional-column-width(1)"/>
      <fo:table-header>
        <fo:table-row>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Prepared by</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Organisation</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Signature</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Date</xsl:with-param>
          </xsl:call-template>
        </fo:table-row>
      </fo:table-header>
      <fo:table-body>
        <xsl:apply-templates select="author[not(@role)]" mode="book.approval"/>
      </fo:table-body>
    </fo:table>
  </xsl:if>
  <xsl:if test="author[@role='approval']">
    <fo:table width="100%" border-collapse="collapse" xsl:use-attribute-sets="informal.object.properties">
      <xsl:call-template name="table.frame"/>
      <fo:table-column column-number="1" column-width="proportional-column-width(1)"/>
      <fo:table-column column-number="2" column-width="proportional-column-width(1)"/>
      <fo:table-column column-number="3" column-width="proportional-column-width(1)"/>
      <fo:table-column column-number="4" column-width="proportional-column-width(1)"/>
      <fo:table-header>
        <fo:table-row>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Approved by</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Organisation</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Signature</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Date</xsl:with-param>
          </xsl:call-template>
        </fo:table-row>
      </fo:table-header>
      <fo:table-body>
        <xsl:apply-templates select="author[@role='approval']" mode="book.approval"/>
      </fo:table-body>
    </fo:table>
  </xsl:if>
  <xsl:if test="author[@role='release']">
    <fo:table width="100%" border-collapse="collapse" xsl:use-attribute-sets="informal.object.properties">
      <xsl:call-template name="table.frame"/>
      <fo:table-column column-number="1" column-width="proportional-column-width(1)"/>
      <fo:table-column column-number="2" column-width="proportional-column-width(1)"/>
      <fo:table-column column-number="3" column-width="proportional-column-width(1)"/>
      <fo:table-column column-number="4" column-width="proportional-column-width(1)"/>
      <fo:table-header>
        <fo:table-row>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Released by</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Organisation</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Signature</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Date</xsl:with-param>
          </xsl:call-template>
        </fo:table-row>
      </fo:table-header>
      <fo:table-body>
        <xsl:apply-templates select="author[@role='release']" mode="book.approval"/>
      </fo:table-body>
    </fo:table>
  </xsl:if>
  <fo:block id="idDistList" break-before="page" xsl:use-attribute-sets="titlepage.title.level1.properties">
    <xsl:text>Distribution List</xsl:text>
  </fo:block>
  <fo:table width="100%" border-collapse="collapse" xsl:use-attribute-sets="informal.object.properties">
    <xsl:call-template name="table.frame"/>
    <fo:table-column column-number="1" column-width="proportional-column-width(2)"/>
    <fo:table-column column-number="2" column-width="proportional-column-width(4)"/>
    <fo:table-header>
      <fo:table-row>
        <xsl:call-template name="table-cell">
          <xsl:with-param name="string">Designation</xsl:with-param>
        </xsl:call-template>
        <xsl:call-template name="table-cell">
          <xsl:with-param name="string">Name</xsl:with-param>
        </xsl:call-template>
      </fo:table-row>
    </fo:table-header>
    <fo:table-body>
      <xsl:apply-templates select="author[not(preceding-sibling::author/affiliation = child::affiliation)]"
          mode="book.distrib"/>
      <fo:table-row>
        <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
          <fo:block>Total:</fo:block>
        </fo:table-cell>
        <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
          <fo:block text-align="right"><xsl:value-of select="count(author)"/></fo:block>
        </fo:table-cell>
      </fo:table-row>
    </fo:table-body>
  </fo:table>
</xsl:template>

<xsl:template match="revhistory" mode="titlepage.mode">
  <fo:block id="idChgRec" xsl:use-attribute-sets="titlepage.title.level1.properties">
    <xsl:text>Change Record</xsl:text>
  </fo:block>

  <fo:block space-before="0.5em" font-family="{$body.font.family}"
      font-size="{$body.font.size}">
    <fo:table width="100%">
      <xsl:call-template name="table.frame"/>
      <fo:table-column column-number="1" column-width="proportional-column-width(1)"/>
      <fo:table-column column-number="2" column-width="proportional-column-width(1)"/>
      <fo:table-column column-number="3" column-width="proportional-column-width(5)"/>
      <fo:table-column column-number="4" column-width="proportional-column-width(1)"/>
      <fo:table-header>
        <fo:table-row>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Date</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Issue/Rev</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Description</xsl:with-param>
          </xsl:call-template>
          <xsl:call-template name="table-cell">
            <xsl:with-param name="string">Initials</xsl:with-param>
          </xsl:call-template>
        </fo:table-row>
      </fo:table-header>
      <fo:table-body>
        <xsl:apply-templates mode="titlepage.mode"/>
      </fo:table-body>
    </fo:table>
  </fo:block>
</xsl:template>

<xsl:template match="revhistory/revision" mode="titlepage.mode">
  <xsl:variable name="revdate"   select=".//date"/>
  <xsl:variable name="revnumber" select=".//revnumber"/>
  <xsl:variable name="revremark" select=".//revremark|.//revdescription"/>
  <xsl:variable name="revauthor" select=".//authorinitials"/>
  <fo:table-row>
    <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'bottom'"/>
      </xsl:call-template>
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'right'"/>
      </xsl:call-template>
      <fo:block>
        <xsl:apply-templates select="$revdate[1]" mode="titlepage.mode"/>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'bottom'"/>
      </xsl:call-template>
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'right'"/>
      </xsl:call-template>
      <fo:block>
        <xsl:apply-templates select="$revnumber[1]" mode="titlepage.mode"/>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'bottom'"/>
      </xsl:call-template>
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'right'"/>
      </xsl:call-template>
      <fo:block>
        <xsl:apply-templates select="$revremark[1]" mode="titlepage.mode"/>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell xsl:use-attribute-sets="table.cell.padding">
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'bottom'"/>
      </xsl:call-template>
      <xsl:call-template name="border">
        <xsl:with-param name="side" select="'right'"/>
      </xsl:call-template>
      <fo:block>
        <xsl:apply-templates select="$revauthor[1]" mode="titlepage.mode"/>
      </fo:block>
    </fo:table-cell>
  </fo:table-row>
</xsl:template>

<xsl:template match="bibliography">
  <xsl:if test="not(preceding-sibling::bibliography)">
    <xsl:variable name="id">
      <xsl:call-template name="object.id"/>
    </xsl:variable>
    <xsl:variable name="master-reference">
      <xsl:call-template name="select.pagemaster"/>
    </xsl:variable>
    <fo:page-sequence hyphenate="{$hyphenate}"
        master-reference="{$master-reference}" format="i">
      <xsl:attribute name="language">
        <xsl:call-template name="l10n.language"/>
      </xsl:attribute>

      <xsl:apply-templates select="." mode="running.head.mode">
        <xsl:with-param name="master-reference" select="$master-reference"/>
      </xsl:apply-templates>
      <xsl:apply-templates select="." mode="running.foot.mode">
        <xsl:with-param name="master-reference" select="$master-reference"/>
      </xsl:apply-templates>

      <fo:flow flow-name="xsl-region-body">
        <fo:block id="{$id}-level1" xsl:use-attribute-sets="titlepage.title.level1.properties">
          <xsl:text>Related Documents</xsl:text>
        </fo:block>
        <xsl:call-template name="bibliography.title"/>
        <xsl:apply-templates/>
        <xsl:for-each select="following-sibling::bibliography">
          <xsl:call-template name="bibliography.title"/>
          <xsl:apply-templates/>
        </xsl:for-each>
      </fo:flow>
    </fo:page-sequence>
  </xsl:if>
</xsl:template>

<xsl:template name="bibliography.title">
  <xsl:variable name="id">
    <xsl:call-template name="object.id"/>
  </xsl:variable>
  <fo:block id="{$id}" margin-left="{$title.margin.left}" font-size="12pt"
      font-family="{$title.font.family}" font-weight="bold">
    <xsl:call-template name="component.title">
      <xsl:with-param name="node" select="."/>
    </xsl:call-template>
  </fo:block>
</xsl:template>

<!-- this produces correct PDF bookmarks using FOP extensions -->
<xsl:template match="bibliography" mode="fop.outline">
  <xsl:variable name="id">
    <xsl:call-template name="object.id"/>
  </xsl:variable>
  <xsl:if test="not(preceding-sibling::bibliography)">
    <fox:outline internal-destination="{$id}-level1">
      <fox:label>Related Documents</fox:label>
        <xsl:for-each select=".|following-sibling::bibliography">
          <xsl:variable name="bid">
            <xsl:call-template name="object.id"/>
          </xsl:variable>
          <xsl:variable name="bookmark-label">
            <xsl:apply-templates select="." mode="object.title.markup"/>
          </xsl:variable>
          <fox:outline internal-destination="{$bid}">
            <fox:label>
              <xsl:value-of select="normalize-space(translate($bookmark-label, $a-dia, $a-asc))"/>
            </fox:label>
          </fox:outline>
        </xsl:for-each>
    </fox:outline>
  </xsl:if>
</xsl:template>

<xsl:template name="glossary.titlepage">
  <!-- duplicate id from page-sequence to work-around FOP bug -->
  <xsl:variable name="id">
    <xsl:call-template name="object.id">
      <xsl:with-param name="object" select="ancestor-or-self::glossary[1]"/>
    </xsl:call-template>
  </xsl:variable>
  <fo:block id="{$id}" xsl:use-attribute-sets="titlepage.title.level1.properties">
    <xsl:call-template name="component.title">
      <xsl:with-param name="node" select="ancestor-or-self::glossary[1]"/>
    </xsl:call-template>
  </fo:block>
</xsl:template>

<xsl:template name="table.of.contents.titlepage.recto">
  <fo:block xsl:use-attribute-sets="titlepage.title.level1.properties">
    <xsl:text>Contents</xsl:text>
  </fo:block>
</xsl:template>

<!-- exclude from table of contents -->
<xsl:template match="glossary|bibliography" mode="toc"/>

<xsl:template name="page.number.format">
  <xsl:param name="element" select="local-name(.)"/>

  <xsl:choose>
    <xsl:when test="$element = 'book'">i</xsl:when>
    <xsl:when test="$element = 'toc'">i</xsl:when>
    <xsl:when test="$element = 'glossary'">i</xsl:when>
    <xsl:otherwise>1</xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- templates for PDF bookmarks using FOP extensions -->
<xsl:template match="book" mode="fop.outline">
  <xsl:variable name="id">
    <xsl:call-template name="object.id"/>
  </xsl:variable>
  <xsl:apply-templates select="bookinfo/revhistory" mode="fop.outline"/>
  <xsl:apply-templates select="bookinfo/authorgroup" mode="fop.outline"/>
  <xsl:apply-templates select="bookinfo/abstract" mode="fop.outline"/>
  <fox:outline internal-destination="toc...{$id}">
    <fox:label>Contents</fox:label>
  </fox:outline>
  <xsl:apply-templates select="glossary" mode="fop.outline"/>
  <xsl:apply-templates select="bibliography" mode="fop.outline"/>
  <xsl:apply-templates select="toc|lot|preface|chapter|reference|part|article|appendix|index|setindex|colophon" mode="fop.outline"/>
</xsl:template>

<xsl:template match="bookinfo/authorgroup" mode="fop.outline">
  <fox:outline internal-destination="idDocApp">
    <fox:label>Document Approval</fox:label>
  </fox:outline>
  <fox:outline internal-destination="idDistList">
    <fox:label>Distribution List</fox:label>
  </fox:outline>
</xsl:template>

<xsl:template match="bookinfo/abstract" mode="fop.outline">
  <fox:outline internal-destination="idAbstract">
    <fox:label>Abstract</fox:label>
  </fox:outline>
</xsl:template>

<xsl:template match="bookinfo/revhistory" mode="fop.outline">
  <fox:outline internal-destination="idChgRec">
    <fox:label>Change Record</fox:label>
  </fox:outline>
</xsl:template>

<!-- don't use italic for inline glossterms -->
<xsl:template name="inline.italicseq">
  <xsl:param name="content">
    <xsl:apply-templates/>
  </xsl:param>
  <fo:inline>
    <xsl:if test="name() != 'glossterm'">
      <xsl:attribute name="font-style">italic</xsl:attribute>
    </xsl:if>
    <xsl:copy-of select="$content"/>
  </fo:inline>
</xsl:template>

</xsl:stylesheet>
